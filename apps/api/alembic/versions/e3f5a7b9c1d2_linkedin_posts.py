"""fila de posts do LinkedIn

Revision ID: e3f5a7b9c1d2
Revises: d8e2f4a6b1c3
Create Date: 2026-10-22 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'e3f5a7b9c1d2'
down_revision = 'd8e2f4a6b1c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'linkedin_posts',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('tenant_id', sa.Uuid(), nullable=False),
        sa.Column('texto', sa.Text(), nullable=False),
        sa.Column('link', sa.String(length=500), nullable=True),
        sa.Column('publicar_em', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('post_urn', sa.String(length=200), nullable=True),
        sa.Column('erro', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('linkedin_posts')
