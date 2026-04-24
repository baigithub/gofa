from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.order_state_machine import transition_order_status
from ..models import Order, OrderStatusLog, User
from ..schemas.order import CreateOrderRequest


def _log_status(db: Session, order_id: str, from_status: str | None, to_status: str, note: str | None = None) -> None:
    db.add(
        OrderStatusLog(
            order_id=order_id,
            from_status=from_status,
            to_status=to_status,
            note=note,
        )
    )


def create_order(db: Session, payload: CreateOrderRequest) -> Order:
    user = db.execute(select(User).where(User.id == payload.user_id)).scalar_one_or_none()
    if user is None:
        raise ValueError("用户不存在")

    now = datetime.utcnow()
    order = Order(
        user_id=payload.user_id,
        order_type=payload.order_type,
        status="pending_pay",
        pickup_address=payload.pickup_address,
        delivery_address=payload.delivery_address,
        contact_phone=payload.contact_phone,
        remark=payload.remark,
        amount_cents=payload.amount_cents,
        created_at=now,
        updated_at=now,
        required_completed_at=now + timedelta(hours=2),
    )
    db.add(order)
    db.flush()
    _log_status(db, order.id, None, "pending_pay", "订单创建")
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session, user_id: str | None = None) -> list[Order]:
    stmt = select(Order).order_by(Order.created_at.desc())
    if user_id:
        stmt = stmt.where(Order.user_id == user_id)
    return list(db.execute(stmt).scalars().all())


def get_order(db: Session, order_id: str) -> Order | None:
    return db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()


def cancel_order(db: Session, order_id: str) -> bool:
    order = get_order(db, order_id)
    if order is None:
        raise ValueError("订单不存在")
    transition_order_status(db, order, "cancelled", "用户取消订单")
    db.commit()
    return True

