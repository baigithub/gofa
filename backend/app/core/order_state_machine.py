from __future__ import annotations

from typing import Dict, Set

from sqlalchemy.orm import Session

from ..models import Order, OrderStatusLog

STATE_TRANSITIONS: Dict[str, Set[str]] = {
    "pending_pay": {"pending_take", "cancelled"},
    "pending_take": {"accepted", "cancelled"},
    "accepted": {"delivering", "completed", "cancelled"},
    "delivering": {"completed", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}


def can_transition(from_status: str, to_status: str) -> bool:
    return to_status in STATE_TRANSITIONS.get(from_status, set())


def transition_order_status(
    db: Session,
    order: Order,
    to_status: str,
    note: str | None = None,
) -> None:
    from_status = order.status
    if from_status == to_status:
        return
    if not can_transition(from_status, to_status):
        raise ValueError(f"非法状态流转: {from_status} -> {to_status}")

    order.status = to_status
    db.add(
        OrderStatusLog(
            order_id=order.id,
            from_status=from_status,
            to_status=to_status,
            note=note,
        )
    )

