"""pautas: apuração do Jornalista (fontes, selo, formatos), relevância e urgência

Revision ID: b4d6f8a0c2e3
Revises: a3c5e7f9b1d2
Create Date: 2026-10-08 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b4d6f8a0c2e3'
down_revision = 'a3c5e7f9b1d2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('pautas', sa.Column('apuracao', sa.JSON(), nullable=True))
    op.add_column('pautas', sa.Column('relevancia', sa.Integer(), nullable=True))
    op.add_column('pautas', sa.Column('urgencia', sa.String(length=10), nullable=True))


def downgrade() -> None:
    op.drop_column('pautas', 'urgencia')
    op.drop_column('pautas', 'relevancia')
    op.drop_column('pautas', 'apuracao')
