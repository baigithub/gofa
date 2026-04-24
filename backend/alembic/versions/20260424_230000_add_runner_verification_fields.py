"""add runner verification fields

Revision ID: 20260424_230000
Revises: 20260424_225500
Create Date: 2026-04-24 23:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "20260424_230000"
down_revision = "20260424_225500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("runner_profiles")}

    if "verification_status" not in columns:
        op.add_column(
            "runner_profiles",
            sa.Column("verification_status", sa.String(length=20), nullable=False, server_default=sa.text("'pending'")),
        )
        op.alter_column("runner_profiles", "verification_status", server_default=None)

    if "rejection_reason" not in columns:
        op.add_column(
            "runner_profiles",
            sa.Column("rejection_reason", sa.String(length=500), nullable=True),
        )
    if "reviewed_by" not in columns:
        op.add_column(
            "runner_profiles",
            sa.Column("reviewed_by", sa.CHAR(length=36), nullable=True),
        )
    if "reviewed_at" not in columns:
        op.add_column(
            "runner_profiles",
            sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        )
    if "is_verified" not in columns:
        op.add_column(
            "runner_profiles",
            sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        )
        op.alter_column("runner_profiles", "is_verified", server_default=None)

    # foreign key may not exist in partially migrated DBs
    fk_names = {fk["name"] for fk in inspector.get_foreign_keys("runner_profiles")}
    if "fk_runner_profiles_reviewed_by" not in fk_names:
        op.create_foreign_key(
            "fk_runner_profiles_reviewed_by",
            "runner_profiles",
            "users",
            ["reviewed_by"],
            ["id"],
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("runner_profiles")}
    fk_names = {fk["name"] for fk in inspector.get_foreign_keys("runner_profiles")}

    if "fk_runner_profiles_reviewed_by" in fk_names:
        op.drop_constraint("fk_runner_profiles_reviewed_by", "runner_profiles", type_="foreignkey")
    if "is_verified" in columns:
        op.drop_column("runner_profiles", "is_verified")
    if "reviewed_at" in columns:
        op.drop_column("runner_profiles", "reviewed_at")
    if "reviewed_by" in columns:
        op.drop_column("runner_profiles", "reviewed_by")
    if "rejection_reason" in columns:
        op.drop_column("runner_profiles", "rejection_reason")
    if "verification_status" in columns:
        op.drop_column("runner_profiles", "verification_status")
