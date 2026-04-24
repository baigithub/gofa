from typing import Optional

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from ..core import error_codes
from ..core.db import get_db
from ..core.exceptions import ApiException
from ..core.response import success
from ..schemas.order import CancelOrderResponse, CreateOrderRequest, OrderResponse
from ..services.order_service import cancel_order, create_order, get_order, list_orders

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post("")
def create_order_api(
    payload: CreateOrderRequest = Body(
        ...,
        examples={
            "pickup-order": {
                "summary": "创建帮取快递订单",
                "value": {
                    "user_id": "3b2f3f5b-3af5-4cf0-bf2e-3f0aa52db31a",
                    "order_type": "pickup",
                    "pickup_address": "北门驿站",
                    "delivery_address": "1号宿舍楼",
                    "contact_phone": "13800138000",
                    "remark": "请放宿管处",
                    "amount_cents": 1000,
                },
            }
        },
    ),
    db: Session = Depends(get_db),
):
    try:
        order = create_order(db, payload)
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(OrderResponse.model_validate(order).model_dump())


@router.get("")
def list_orders_api(user_id: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    orders = list_orders(db, user_id=user_id)
    data = [OrderResponse.model_validate(order).model_dump() for order in orders]
    return success(data)


@router.get("/{order_id}")
def get_order_api(order_id: str, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if order is None:
        raise ApiException(error_codes.NOT_FOUND, "订单不存在", status_code=404)
    return success(OrderResponse.model_validate(order).model_dump())


@router.post("/{order_id}/cancel")
def cancel_order_api(order_id: str, db: Session = Depends(get_db)):
    try:
        cancel_order(db, order_id)
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(CancelOrderResponse(success=True).model_dump())

