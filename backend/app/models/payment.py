from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("orders.id"), nullable=False, unique=True, index=True)

    provider: Mapped[str] = mapped_column(String(20), nullable=False, default="wechat")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="created", index=True)

    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    provider_txn_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

