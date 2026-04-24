from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=False, index=True)
    runner_id: Mapped[Optional[str]] = mapped_column(
        CHAR(36),
        ForeignKey("runner_profiles.id"),
        nullable=True,
        index=True,
    )

    order_type: Mapped[str] = mapped_column(String(20), nullable=False)  # pickup/buy/errand
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending_pay", index=True)

    pickup_address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    delivery_address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    contact_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    required_completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

