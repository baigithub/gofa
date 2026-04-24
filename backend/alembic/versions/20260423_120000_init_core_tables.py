"""init core tables

Revision ID: 20260423_120000
Revises:
Create Date: 2026-04-23 12:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "20260423_120000"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", mysql.CHAR(36), primary_key=True),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("nickname", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("phone", name="uq_users_phone"),
    )
    op.create_index("ix_users_phone", "users", ["phone"], unique=False)

    op.create_table(
        "runner_profiles",
        sa.Column("id", mysql.CHAR(36), primary_key=True),
        sa.Column("user_id", mysql.CHAR(36), nullable=False),
        sa.Column("student_no", sa.String(32), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_runner_profiles_user_id"),
        sa.UniqueConstraint("user_id", name="uq_runner_profiles_user_id"),
    )
    op.create_index("ix_runner_profiles_user_id", "runner_profiles", ["user_id"], unique=False)

    op.create_table(
        "addresses",
        sa.Column("id", mysql.CHAR(36), primary_key=True),
        sa.Column("user_id", mysql.CHAR(36), nullable=False),
        sa.Column("label", sa.String(50), nullable=True),
        sa.Column("detail", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_addresses_user_id"),
    )
    op.create_index("ix_addresses_user_id", "addresses", ["user_id"], unique=False)

    op.create_table(
        "orders",
        sa.Column("id", mysql.CHAR(36), primary_key=True),
        sa.Column("user_id", mysql.CHAR(36), nullable=False),
        sa.Column("runner_id", mysql.CHAR(36), nullable=True),
        sa.Column("order_type", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("pickup_address", sa.String(255), nullable=True),
        sa.Column("delivery_address", sa.String(255), nullable=True),
        sa.Column("contact_phone", sa.String(20), nullable=False),
        sa.Column("remark", sa.Text(), nullable=True),
        sa.Column("amount_cents", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_orders_user_id"),
        sa.ForeignKeyConstraint(["runner_id"], ["runner_profiles.id"], name="fk_orders_runner_id"),
    )
    op.create_index("ix_orders_user_id", "orders", ["user_id"], unique=False)
    op.create_index("ix_orders_runner_id", "orders", ["runner_id"], unique=False)
    op.create_index("ix_orders_status", "orders", ["status"], unique=False)

    op.create_table(
        "order_status_logs",
        sa.Column("id", mysql.CHAR(36), primary_key=True),
        sa.Column("order_id", mysql.CHAR(36), nullable=False),
        sa.Column("from_status", sa.String(20), nullable=True),
        sa.Column("to_status", sa.String(20), nullable=False),
        sa.Column("note", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], name="fk_order_status_logs_order_id"),
    )
    op.create_index("ix_order_status_logs_order_id", "order_status_logs", ["order_id"], unique=False)

    op.create_table(
        "payments",
        sa.Column("id", mysql.CHAR(36), primary_key=True),
        sa.Column("order_id", mysql.CHAR(36), nullable=False),
        sa.Column("provider", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("amount_cents", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("provider_txn_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], name="fk_payments_order_id"),
        sa.UniqueConstraint("order_id", name="uq_payments_order_id"),
    )
    op.create_index("ix_payments_order_id", "payments", ["order_id"], unique=False)
    op.create_index("ix_payments_status", "payments", ["status"], unique=False)

    op.create_table(
        "messages",
        sa.Column("id", mysql.CHAR(36), primary_key=True),
        sa.Column("user_id", mysql.CHAR(36), nullable=False),
        sa.Column("order_id", mysql.CHAR(36), nullable=True),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_messages_user_id"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], name="fk_messages_order_id"),
    )
    op.create_index("ix_messages_user_id", "messages", ["user_id"], unique=False)
    op.create_index("ix_messages_order_id", "messages", ["order_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_messages_order_id", table_name="messages")
    op.drop_index("ix_messages_user_id", table_name="messages")
    op.drop_table("messages")

    op.drop_index("ix_payments_status", table_name="payments")
    op.drop_index("ix_payments_order_id", table_name="payments")
    op.drop_table("payments")

    op.drop_index("ix_order_status_logs_order_id", table_name="order_status_logs")
    op.drop_table("order_status_logs")

    op.drop_index("ix_orders_status", table_name="orders")
    op.drop_index("ix_orders_runner_id", table_name="orders")
    op.drop_index("ix_orders_user_id", table_name="orders")
    op.drop_table("orders")

    op.drop_index("ix_addresses_user_id", table_name="addresses")
    op.drop_table("addresses")

    op.drop_index("ix_runner_profiles_user_id", table_name="runner_profiles")
    op.drop_table("runner_profiles")

    op.drop_index("ix_users_phone", table_name="users")
    op.drop_table("users")

