import uuid
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

def uid() -> str:
    return str(uuid.uuid4())

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: str = Field(default_factory=uid, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=254)
    password_hash: str
    display_name: str = Field(max_length=180)
    is_active: bool = True

class Institution(SQLModel, table=True):
    __tablename__ = 'institutions'
    id: str = Field(default_factory=uid, primary_key=True)
    code: str = Field(unique=True, max_length=40)
    name: str = Field(max_length=180)
    created_at: datetime = Field(default_factory=utcnow)

class Membership(SQLModel, table=True):
    __tablename__ = 'memberships'
    __table_args__ = (UniqueConstraint('user_id','institution_id', name='uq_membership_user_institution'),)
    id: str = Field(default_factory=uid, primary_key=True)
    user_id: str = Field(foreign_key='users.id', index=True)
    institution_id: str = Field(foreign_key='institutions.id', index=True)
    role: str = Field(max_length=30)  # administrator, teacher, student

class Program(SQLModel, table=True):
    __tablename__ = 'programs'
    __table_args__ = (UniqueConstraint('institution_id','code', name='uq_program_scope_code'),)
    id: str = Field(default_factory=uid, primary_key=True)
    institution_id: str = Field(foreign_key='institutions.id', index=True)
    code: str = Field(max_length=40)
    title: str = Field(max_length=200)

class Competency(SQLModel, table=True):
    __tablename__ = 'competencies'
    __table_args__ = (UniqueConstraint('institution_id','code', name='uq_competency_scope_code'),)
    id: str = Field(default_factory=uid, primary_key=True)
    institution_id: str = Field(foreign_key='institutions.id', index=True)
    program_id: str | None = Field(default=None, foreign_key='programs.id')
    code: str = Field(max_length=40)
    title: str = Field(max_length=200)
    description: str = Field(default='', max_length=2000)
    level: str = Field(default='general', max_length=40)

class AuditEvent(SQLModel, table=True):
    __tablename__ = 'audit_events'
    id: str = Field(default_factory=uid, primary_key=True)
    actor_id: str = Field(foreign_key='users.id')
    institution_id: str | None = Field(default=None, foreign_key='institutions.id')
    action: str = Field(max_length=100)
    target_id: str = Field(max_length=80)
    created_at: datetime = Field(default_factory=utcnow)
