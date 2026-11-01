from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.config import settings
from app.database import get_session
from app.models import User, Institution, Membership, Program, Competency, AuditEvent
from app.schemas import LoginInput, InstitutionInput, CompetencyInput, ProgramInput
from app.security import current_user, require_scope, token_for, verify_password

app = FastAPI(title='SIVEFOC API', version='0.2.0', description='Núcleo inicial; NO listo para producción')
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(',')],
                   allow_credentials=False, allow_methods=['GET','POST'], allow_headers=['Authorization','Content-Type','X-Institution-Id'])

@app.get('/health')
def health():
    return {'status':'ok', 'version':'0.2.0'}

@app.post('/v1/auth/login')
def login(payload: LoginInput, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == payload.email.lower())).first()
    if not user or not verify_password(payload.password, user.password_hash) or not user.is_active:
        raise HTTPException(401, 'Credenciales inválidas')
    return {'access_token':token_for(user.id),'token_type':'bearer'}

@app.get('/v1/me')
def me(user: User = Depends(current_user), session: Session = Depends(get_session)):
    memberships = session.exec(select(Membership).where(Membership.user_id == user.id)).all()
    return {'id':user.id, 'email':user.email, 'name':user.display_name,
            'memberships':[{'institution_id':m.institution_id,'role':m.role} for m in memberships]}

@app.get('/v1/institutions', response_model=list[Institution])
def institutions(user: User = Depends(current_user), session: Session = Depends(get_session)):
    ids = session.exec(select(Membership.institution_id).where(Membership.user_id == user.id)).all()
    if not ids: return []
    return session.exec(select(Institution).where(Institution.id.in_(ids)).order_by(Institution.name)).all()

@app.get('/v1/programs', response_model=list[Program])
def programs(x_institution_id: str = Header(), user: User = Depends(current_user), session: Session = Depends(get_session)):
    require_scope(x_institution_id,user,session,{'administrator','teacher','student'})
    return session.exec(select(Program).where(Program.institution_id == x_institution_id).order_by(Program.code)).all()

@app.post('/v1/programs', response_model=Program, status_code=201)
def create_program(data: ProgramInput, x_institution_id: str = Header(), user: User = Depends(current_user), session: Session = Depends(get_session)):
    require_scope(x_institution_id,user,session,{'administrator'})
    obj = Program(institution_id=x_institution_id, **data.model_dump())
    return commit_item(session,obj,user.id,x_institution_id,'program.created')

@app.get('/v1/competencies', response_model=list[Competency])
def competencies(x_institution_id: str = Header(), user: User = Depends(current_user), session: Session = Depends(get_session)):
    require_scope(x_institution_id,user,session,{'administrator','teacher','student'})
    return session.exec(select(Competency).where(Competency.institution_id == x_institution_id).order_by(Competency.code)).all()

@app.post('/v1/competencies', response_model=Competency, status_code=201)
def create_competency(data: CompetencyInput, x_institution_id: str = Header(), user: User = Depends(current_user), session: Session = Depends(get_session)):
    require_scope(x_institution_id,user,session,{'administrator','teacher'})
    if data.program_id:
        program = session.get(Program,data.program_id)
        if not program or program.institution_id != x_institution_id:
            raise HTTPException(404,'Programa no encontrado en institución')
    obj = Competency(institution_id=x_institution_id, **data.model_dump())
    return commit_item(session,obj,user.id,x_institution_id,'competency.created')

def commit_item(session: Session, obj, actor_id: str, institution_id: str, action: str):
    try:
        session.add(obj)
        session.flush()
        session.add(AuditEvent(actor_id=actor_id,institution_id=institution_id,action=action,target_id=obj.id))
        session.commit()
        session.refresh(obj)
        return obj
    except IntegrityError:
        session.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT,'Código duplicado en ámbito institucional')
