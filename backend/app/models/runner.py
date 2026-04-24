from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class RunnerProfile(Base):
    __tablename__ = "runner_profiles"

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(CHAR(36), ForeignKey("users.id"), unique=True, nullable=False, index=True)

    student_no: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    credential_images: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True, default=None)
    verification_status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    reviewed_by: Mapped[Optional[str]] = mapped_column(CHAR(36), ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", foreign_keys=[user_id], lazy="joined")
    reviewer = relationship("User", foreign_keys=[reviewed_by], lazy="joined")

