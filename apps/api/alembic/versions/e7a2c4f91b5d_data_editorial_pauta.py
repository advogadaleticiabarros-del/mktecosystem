"""data_editorial em pautas

Revision ID: e7a2c4f91b5d
Revises: e7a2c4f6b891
Create Date: 2026-09-29 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'e7a2c4f91b5d'
down_revision = 'e7a2c4f6b891'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('pautas', sa.Column('data_editorial', sa.Date(), nullable=True))
    op.create_index('ix_pautas_data_editorial', 'pautas', ['data_editorial'])


def downgrade() -> None:
    op.drop_index('ix_pautas_data_editorial', table_name='pautas')
    op.drop_column('pautas', 'data_editorial')
