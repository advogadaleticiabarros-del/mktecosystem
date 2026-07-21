"""widen scheduled_posts.platform_post_id for blog URLs

Revision ID: b23b58347cb7
Revises: c5219c39eacb
Create Date: 2026-07-21 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b23b58347cb7'
down_revision = 'c5219c39eacb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('scheduled_posts', 'platform_post_id', type_=sa.String(length=500))


def downgrade() -> None:
    op.alter_column('scheduled_posts', 'platform_post_id', type_=sa.String(length=50))
