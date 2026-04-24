"""add chat and review tables

Revision ID: 20260423_210000
Revises: 20260423_200000
Create Date: 2026-04-23 21:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "20260423_210000"
down_revision = "20260423_200000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_messages",
        sa.Column("id", mysql.CHAR(36), primary_key=True),
        sa.Column("order_id", mysql.CHAR(36), nullable=False),
        sa.Column("sender_user_id", mysql.CHAR(36), nullable=False),
        sa.Column("sender_role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], name="fk_chat_messages_order_id"),
        sa.ForeignKeyConstraint(["sender_user_id"], ["users.id"], name="fk_chat_messages_sender_user_id"),
    )
    op.create_index("ix_chat_messages_order_id", "chat_messages", ["order_id"], unique=False)
    op.create_index("ix_chat_messages_sender_user_id", "chat_messages", ["sender_user_id"], unique=False)

    op.create_table(
        "order_reviews",
        sa.Column("id", mysql.CHAR(36), primary_key=True),
        sa.Column("order_id", mysql.CHAR(36), nullable=False),
        sa.Column("user_id", mysql.CHAR(36), nullable=False),
        sa.Column("runner_id", mysql.CHAR(36), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], name="fk_order_reviews_order_id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_order_reviews_user_id"),
        sa.ForeignKeyConstraint(["runner_id"], ["runner_profiles.id"], name="fk_order_reviews_runner_id"),
        sa.UniqueConstraint("order_id", name="uq_order_reviews_order_id"),
    )
    op.create_index("ix_order_reviews_order_id", "order_reviews", ["order_id"], unique=False)
    op.create_index("ix_order_reviews_user_id", "order_reviews", ["user_id"], unique=False)
    op.create_index("ix_order_reviews_runner_id", "order_reviews", ["runner_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_order_reviews_runner_id", table_name="order_reviews")
    op.drop_index("ix_order_reviews_user_id", table_name="order_reviews")
    op.drop_index("ix_order_reviews_order_id", table_name="order_reviews")
    op.drop_table("order_reviews")

    op.drop_index("ix_chat_messages_sender_user_id", table_name="chat_messages")
    op.drop_index("ix_chat_messages_order_id", table_name="chat_messages")
    op.drop_table("chat_messages")

