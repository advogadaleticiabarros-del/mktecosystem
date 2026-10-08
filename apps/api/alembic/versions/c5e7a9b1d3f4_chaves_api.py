"""cria chaves_api (chaves de serviços externos, criptografadas, cadastradas pelo painel)

Revision ID: c5e7a9b1d3f4
Revises: b4d6f8a0c2e3
Create Date: 2026-10-08 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'c5e7a9b1d3f4'
down_revision = 'b4d6f8a0c2e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'chaves_api',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('tenant_id', sa.Uuid(), nullable=False),
        sa.Column('provedor', sa.String(length=30), nullable=False),
        sa.Column('chave_criptografada', sa.Text(), nullable=False),
        sa.Column('final', sa.String(length=8), nullable=False),
        sa.Column('validada_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'provedor', name='uq_chaves_api_tenant_provedor'),
    )


def downgrade() -> None:
    op.drop_table('chaves_api')
