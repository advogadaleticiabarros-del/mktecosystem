"""alerta de atualidade em pautas e content_pieces

Revision ID: d4f1a8c9e2b3
Revises: b23b58347cb7
Create Date: 2026-07-30 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'd4f1a8c9e2b3'
down_revision = 'b23b58347cb7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('pautas', sa.Column('alerta_atualidade', sa.String(length=500), nullable=True))
    op.add_column('pautas', sa.Column('verificado_em', sa.DateTime(timezone=True), nullable=True))
    op.add_column(
        'content_pieces', sa.Column('alerta_atualidade', sa.String(length=500), nullable=True)
    )
    op.add_column(
        'content_pieces', sa.Column('verificado_em', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('content_pieces', 'verificado_em')
    op.drop_column('content_pieces', 'alerta_atualidade')
    op.drop_column('pautas', 'verificado_em')
    op.drop_column('pautas', 'alerta_atualidade')
