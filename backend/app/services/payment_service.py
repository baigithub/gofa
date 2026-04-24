from __future__ import annotations

import hashlib
import hmac
import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.order_state_machine import transition_order_status
from ..models import Order, Payment


def create_payment(db: Session, order_id: str) -> Payment:
    order = db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()
    if order is None:
        raise ValueError("订单不存在")
    if order.status != "pending_pay":
        raise ValueError("当前订单状态不可支付")

    existing = db.execute(select(Payment).where(Payment.order_id == order_id)).scalar_one_or_none()
    if existing is not None:
        return existing

    payment = Payment(
        order_id=order_id,
        provider="wechat",
        status="created",
        amount_cents=order.amount_cents,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment_status(db: Session, order_id: str) -> str:
    payment = db.execute(select(Payment).where(Payment.order_id == order_id)).scalar_one_or_none()
    if payment is None:
        raise ValueError("支付单不存在")
    return payment.status


def verify_wechat_callback_signature(
    order_id: str,
    provider_txn_id: str,
    status: str,
    timestamp: int,
    nonce: str,
    signature: str,
) -> bool:
    # 5分钟时效窗口，避免重放
    now = int(time.time())
    if abs(now - timestamp) > 300:
        return False

    message = f"{order_id}|{provider_txn_id}|{status}|{timestamp}|{nonce}"
    expected = hmac.new(
        settings.wechat_callback_secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def handle_wechat_callback(db: Session, order_id: str, provider_txn_id: str, status: str) -> bool:
    payment = db.execute(select(Payment).where(Payment.order_id == order_id)).scalar_one_or_none()
    if payment is None:
        raise ValueError("支付单不存在")

    # 幂等：已经成功则直接返回成功
    if payment.status == "success":
        return True

    order = db.execute(select(Order).where(Order.id == order_id)).scalar_one_or_none()
    if order is None:
        raise ValueError("订单不存在")

    if status == "success":
        payment.status = "success"
        payment.provider_txn_id = provider_txn_id
        transition_order_status(db, order, "pending_take", "支付成功回调")
    else:
        payment.status = "failed"
        payment.provider_txn_id = provider_txn_id

    db.commit()
    return True

