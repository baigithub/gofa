"""add user is_enabled

Revision ID: 20260424_232000
Revises: 20260424_231500
Create Date: 2026-04-24 23:20:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "20260424_232000"
down_revision = "20260424_231500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("users")}
    if "is_enabled" not in columns:
        op.add_column(
            "users",
            sa.Column("is_enabled", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        )
        op.alter_column("users", "is_enabled", server_default=None)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("users")}
    if "is_enabled" in columns:
        op.drop_column("users", "is_enabled")
