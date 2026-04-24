"""add runner credential images

Revision ID: 20260424_225500
Revises: 20260423_210000
Create Date: 2026-04-24 22:55:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "20260424_225500"
down_revision = "20260423_210000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("runner_profiles")}
    if "credential_images" not in columns:
        op.add_column(
            "runner_profiles",
            sa.Column("credential_images", sa.String(length=2000), nullable=True),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("runner_profiles")}
    if "credential_images" in columns:
        op.drop_column("runner_profiles", "credential_images")
