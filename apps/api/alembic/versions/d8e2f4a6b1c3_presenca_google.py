"""presença no Google: status das recomendações e posts do Perfil da Empresa

Revision ID: d8e2f4a6b1c3
Revises: c5e7a9b1d3f4
Create Date: 2026-10-22 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'd8e2f4a6b1c3'
down_revision = 'c5e7a9b1d3f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'recomendacoes_status',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('tenant_id', sa.Uuid(), nullable=False),
        sa.Column('chave', sa.String(length=80), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'chave', name='uq_recomendacoes_status_tenant_chave'),
    )
    op.create_table(
        'google_posts',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('tenant_id', sa.Uuid(), nullable=False),
        sa.Column('texto', sa.Text(), nullable=False),
        sa.Column('botao', sa.String(length=20), nullable=True),
        sa.Column('link', sa.String(length=500), nullable=True),
        sa.Column('imagem_url', sa.String(length=500), nullable=True),
        sa.Column('publicar_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('google_name', sa.String(length=300), nullable=True),
        sa.Column('link_publicado', sa.String(length=500), nullable=True),
        sa.Column('erro', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('google_posts')
    op.drop_table('recomendacoes_status')
