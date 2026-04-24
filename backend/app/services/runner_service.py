from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.order_state_machine import transition_order_status
import json

from ..models import ChatMessage, Order, OrderReview, RunnerProfile, User


def _resolve_order(db: Session, order_id: str) -> Order | None:
    if order_id == "latest":
        return db.execute(select(Order).order_by(Order.created_at.desc())).scalar_one_or_none()
    return db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()


def _serialize_images(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
        return []
    return [item for item in data if isinstance(item, str)]


def _dump_images(images: list[str]) -> str:
    return json.dumps([img for img in images if isinstance(img, str)], ensure_ascii=False)


def _to_runner_item(profile: RunnerProfile):
    profile.credential_images = profile.credential_images or "[]"
    return profile


def list_hall_orders(db: Session) -> list[Order]:
    stmt = (
        select(Order)
        .where(Order.status == "pending_take")
        .order_by(Order.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())


def accept_order(db: Session, order_id: str, runner_id: str) -> bool:
    order = db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()
    if order is None:
        raise ValueError("订单不存在")
    runner = db.execute(select(RunnerProfile).where(RunnerProfile.id == runner_id)).scalar_one_or_none()
    if runner is None:
        raise ValueError("跑腿员不存在")
    if runner.verification_status != "approved" or not runner.is_verified:
        raise ValueError("您的认证还在审核中，请耐心等待～")

    order.runner_id = runner_id
    transition_order_status(db, order, "accepted", "跑腿员接单")
    db.commit()
    return True


def delivered_order(db: Session, order_id: str, runner_id: str) -> bool:
    order = db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()
    if order is None:
        raise ValueError("订单不存在")
    if order.runner_id != runner_id:
        raise ValueError("无权限操作此订单")
    transition_order_status(db, order, "completed", "跑腿员确认送达")
    order.completed_at = datetime.utcnow()
    db.commit()
    return True


def list_order_chats(db: Session, order_id: str) -> list[ChatMessage]:
    order = _resolve_order(db, order_id)
    if order is None:
        return []
    stmt = select(ChatMessage).where(ChatMessage.order_id == order.id).order_by(ChatMessage.created_at.asc())
    return list(db.execute(stmt).scalars().all())


def send_order_chat(db: Session, order_id: str, sender_user_id: str, sender_role: str, content: str) -> ChatMessage:
    order = _resolve_order(db, order_id)
    if order is None:
        raise ValueError("订单不存在")

    msg = ChatMessage(
        order_id=order.id,
        sender_user_id=sender_user_id,
        sender_role=sender_role,
        content=content.strip(),
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def submit_review(db: Session, order_id: str, user_id: str, rating: int, comment: str) -> OrderReview:
    order = _resolve_order(db, order_id)
    if order is None:
        raise ValueError("订单不存在")
    if order.user_id != user_id:
        raise ValueError("无权限评价此订单")
    if order.status != "completed":
        raise ValueError("订单未完成，暂不可评价")
    exists = db.execute(select(OrderReview).where(OrderReview.order_id == order.id)).scalar_one_or_none()
    if exists:
        raise ValueError("该订单已评价")
    review = OrderReview(
        order_id=order.id,
        user_id=user_id,
        runner_id=order.runner_id,
        rating=rating,
        comment=comment.strip(),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_review(db: Session, order_id: str) -> OrderReview | None:
    order = _resolve_order(db, order_id)
    if order is None:
        return None
    return db.execute(select(OrderReview).where(OrderReview.order_id == order.id)).scalar_one_or_none()

