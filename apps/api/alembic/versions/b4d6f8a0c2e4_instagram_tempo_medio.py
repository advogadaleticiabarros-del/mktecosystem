"""tempo médio assistido dos Reels

Revision ID: b4d6f8a0c2e4
Revises: e3f5a7b9c1d2
Create Date: 2026-10-27 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b4d6f8a0c2e4'
down_revision = 'e3f5a7b9c1d2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('instagram_posts', sa.Column('tempo_medio_ms', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('instagram_posts', 'tempo_medio_ms')
