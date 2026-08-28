"""conteudo_bruto em pautas (import do Radar Jurídico via CLI)

Revision ID: e7a2c4f6b891
Revises: d4f1a8c9e2b3
Create Date: 2026-08-28 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'e7a2c4f6b891'
down_revision = 'd4f1a8c9e2b3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('pautas', sa.Column('conteudo_bruto', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('pautas', 'conteudo_bruto')
