"""add auth fields to user table

Revision ID: a1b2c3d4e5f6
Revises: d2d14bd867de
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'd2d14bd867de'
branch_labels = None
depends_on = None


def upgrade():
    # Add password_hash and role columns
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('role', sa.String(length=50), nullable=True, server_default='user'))


def downgrade():
    # Remove password_hash and role columns
    op.drop_column('users', 'role')
    op.drop_column('users', 'password_hash')
