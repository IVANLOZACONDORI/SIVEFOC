"""Initial SIVEFOC core schema
Revision ID: 0001
Revises:
"""
from alembic import op
from sqlmodel import SQLModel
from app import models  # noqa
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    SQLModel.metadata.create_all(bind=op.get_bind())

def downgrade():
    SQLModel.metadata.drop_all(bind=op.get_bind())
