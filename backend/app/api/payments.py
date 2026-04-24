from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from ..core import error_codes
from ..core.db import get_db
from ..core.exceptions import ApiException
from ..core.response import success
from ..schemas.payment import (
    CallbackResponse,
    CreatePaymentRequest,
    PaymentResponse,
    PaymentStatusResponse,
    WechatCallbackRequest,
)
from ..services.payment_service import (
    create_payment,
    get_payment_status,
    handle_wechat_callback,
    verify_wechat_callback_signature,
)

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


@router.post("/create")
def create_payment_api(
    payload: CreatePaymentRequest = Body(
        ...,
        examples={
            "default": {
                "summary": "创建支付单示例",
                "value": {"order_id": "95c6f1e0-72f8-4d84-b4c2-0860b2f1db95"},
            }
        },
    ),
    db: Session = Depends(get_db),
):
    try:
        payment = create_payment(db, payload.order_id)
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(PaymentResponse.model_validate(payment).model_dump())


@router.get("/{order_id}/status")
def payment_status_api(order_id: str, db: Session = Depends(get_db)):
    try:
        status = get_payment_status(db, order_id)
    except ValueError as exc:
        raise ApiException(error_codes.NOT_FOUND, str(exc), status_code=404) from exc
    return success(PaymentStatusResponse(order_id=order_id, status=status).model_dump())


@router.post("/wechat/callback")
def wechat_callback_api(
    payload: WechatCallbackRequest = Body(
        ...,
        examples={
            "success-callback": {
                "summary": "微信支付成功回调示例",
                "value": {
                    "order_id": "95c6f1e0-72f8-4d84-b4c2-0860b2f1db95",
                    "provider_txn_id": "wx_txn_20260423_001",
                    "status": "success",
                    "timestamp": 1713840000,
                    "nonce": "nonce123",
                    "signature": "hmac_sha256_signature_hex",
                },
            }
        },
    ),
    db: Session = Depends(get_db),
):
    is_valid = verify_wechat_callback_signature(
        order_id=payload.order_id,
        provider_txn_id=payload.provider_txn_id,
        status=payload.status,
        timestamp=payload.timestamp,
        nonce=payload.nonce,
        signature=payload.signature,
    )
    if not is_valid:
        raise ApiException(error_codes.UNAUTHORIZED, "无效签名", status_code=401)

    try:
        handle_wechat_callback(
            db,
            order_id=payload.order_id,
            provider_txn_id=payload.provider_txn_id,
            status=payload.status,
        )
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(CallbackResponse(success=True).model_dump())

