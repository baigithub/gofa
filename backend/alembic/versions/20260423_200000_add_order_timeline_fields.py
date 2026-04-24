"""add order timeline fields

Revision ID: 20260423_200000
Revises: 20260423_190000
Create Date: 2026-04-23 20:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260423_200000"
down_revision = "20260423_190000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("orders", sa.Column("required_completed_at", sa.DateTime(), nullable=True))
    op.add_column("orders", sa.Column("completed_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("orders", "completed_at")
    op.drop_column("orders", "required_completed_at")

