"""001_phase_b_institutes_and_rbac

Revision ID: 001_phase_b
Revises: 
Create Date: 2026-09-29 15:58:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_phase_b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Ensure institutes table fields
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    if 'institutes' not in existing_tables:
        op.create_table(
            'institutes',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('code', sa.String(50), unique=True, index=True, nullable=False),
            sa.Column('name', sa.String(255), nullable=False),
            sa.Column('institute_type', sa.String(100), default="Regional Institute of Cooperative Management"),
            sa.Column('region', sa.String(100), nullable=False),
            sa.Column('state', sa.String(100), nullable=False),
            sa.Column('city', sa.String(100), nullable=False),
            sa.Column('address', sa.Text(), nullable=True),
            sa.Column('contact_email', sa.String(255), nullable=True),
            sa.Column('contact_phone', sa.String(50), nullable=True),
            sa.Column('director_name', sa.String(255), nullable=True, default="Dr. NCCT Director"),
            sa.Column('total_training_capacity', sa.Integer(), default=500),
            sa.Column('is_active', sa.Boolean(), default=True),
            sa.Column('sync_status', sa.String(50), default="HEALTHY"),
            sa.Column('last_synced_at', sa.DateTime(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True)
        )
    else:
        inst_columns = [col['name'] for col in inspector.get_columns('institutes')]
        if 'director_name' not in inst_columns:
            op.add_column('institutes', sa.Column('director_name', sa.String(255), nullable=True, default="Dr. NCCT Director"))
        if 'total_training_capacity' not in inst_columns:
            op.add_column('institutes', sa.Column('total_training_capacity', sa.Integer(), default=500))

    # 2. Ensure institute_id column on users
    if 'users' in existing_tables:
        user_columns = [col['name'] for col in inspector.get_columns('users')]
        if 'institute_id' not in user_columns:
            op.add_column('users', sa.Column('institute_id', sa.String(36), sa.ForeignKey('institutes.id'), nullable=True))

def downgrade() -> None:
    pass
