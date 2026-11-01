from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select
from app.config import settings
from app.database import get_session
from app.models import User, Membership

hasher = PasswordHash.recommended()
bearer = HTTPBearer(auto_error=False)

def password_hash(password: str) -> str:
    return hasher.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return hasher.verify(password, hashed)

def token_for(user_id: str) -> str:
    if len(settings.secret_key) < 32:
        raise RuntimeError('SECRET_KEY must contain at least 32 characters')
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    return jwt.encode({'sub': user_id, 'exp': exp}, settings.secret_key, algorithm='HS256')

def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
                 session: Session = Depends(get_session)) -> User:
    if not credentials:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Autenticación requerida')
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=['HS256'])
        user = session.get(User, payload['sub'])
    except (jwt.InvalidTokenError, KeyError, TypeError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Token inválido')
    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Usuario no autorizado')
    return user

def require_scope(institution_id: str, user: User, session: Session, roles: set[str]) -> Membership:
    membership = session.exec(select(Membership).where(
        Membership.institution_id == institution_id, Membership.user_id == user.id)).first()
    if not membership or membership.role not in roles:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Sin permiso institucional')
    return membership
