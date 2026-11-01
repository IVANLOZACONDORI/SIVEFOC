"""Single institution and demo administrator bootstrap; NEVER deploy demo credentials to production."""
import os
from sqlmodel import Session, select
from app.database import engine
from app.models import User, Institution, Membership
from app.security import password_hash

def main():
    email = os.getenv('DEMO_BOOTSTRAP_EMAIL', '').lower()
    password = os.getenv('DEMO_BOOTSTRAP_PASSWORD','')
    if not email or len(password) < 12:
        raise SystemExit('Provide DEMO_BOOTSTRAP_EMAIL and DEMO_BOOTSTRAP_PASSWORD >= 12 chars')
    with Session(engine) as s:
        if s.exec(select(User).where(User.email==email)).first():
            raise SystemExit('Bootstrap account already exists; no changes')
        institution = s.exec(select(Institution).where(Institution.code=='DEMO')).first()
        if not institution:
            institution = Institution(code='DEMO',name='Institución de demostración (no oficial)')
            s.add(institution); s.flush()
        user = User(email=email,password_hash=password_hash(password),display_name='Administrador de demostración')
        s.add(user); s.flush()
        s.add(Membership(user_id=user.id,institution_id=institution.id,role='administrator'))
        s.commit()
        print('Demo admin created; institution ID:',institution.id)
if __name__=='__main__': main()
