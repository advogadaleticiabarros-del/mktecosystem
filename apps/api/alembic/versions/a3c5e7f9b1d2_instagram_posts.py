"""cria instagram_posts (cada publicação com suas métricas, para a Análise)

Revision ID: a3c5e7f9b1d2
Revises: f1b3d5a7c9e2
Create Date: 2026-10-08 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a3c5e7f9b1d2'
down_revision = 'f1b3d5a7c9e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'instagram_posts',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('tenant_id', sa.Uuid(), nullable=False),
        sa.Column('media_id', sa.String(length=40), nullable=False),
        sa.Column('publicado_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('formato', sa.String(length=20), nullable=False),
        sa.Column('area', sa.String(length=30), nullable=False),
        sa.Column('legenda', sa.Text(), nullable=True),
        sa.Column('permalink', sa.String(length=255), nullable=True),
        sa.Column('alcance', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('visualizacoes', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('curtidas', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('comentarios', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('compartilhamentos', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('salvamentos', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('interacoes', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('seguidores_ganhos', sa.Integer(), nullable=True),
        sa.Column('visitas_perfil', sa.Integer(), nullable=True),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'media_id', name='uq_instagram_posts_tenant_media'),
    )
    op.create_index('ix_instagram_posts_tenant_id', 'instagram_posts', ['tenant_id'])


def downgrade() -> None:
    op.drop_index('ix_instagram_posts_tenant_id', table_name='instagram_posts')
    op.drop_table('instagram_posts')
