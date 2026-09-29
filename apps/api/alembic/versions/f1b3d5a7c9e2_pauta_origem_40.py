"""amplia pautas.origem para 40 caracteres

'radar_juridico_manchete'/'radar_juridico_satelite' têm 23 caracteres e
estouravam o String(20) no Postgres (SQLite dos testes não valida tamanho).

Revision ID: f1b3d5a7c9e2
Revises: e7a2c4f91b5d
Create Date: 2026-09-29 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'f1b3d5a7c9e2'
down_revision = 'e7a2c4f91b5d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('pautas', 'origem', type_=sa.String(length=40), existing_type=sa.String(length=20))


def downgrade() -> None:
    op.alter_column('pautas', 'origem', type_=sa.String(length=20), existing_type=sa.String(length=40))
