import hashlib
import hmac
import time

import pytest
from backend.app.core.config import settings


def sign_callback(order_id: str, provider_txn_id: str, status: str, timestamp: int, nonce: str) -> str:
    message = f"{order_id}|{provider_txn_id}|{status}|{timestamp}|{nonce}"
    return hmac.new(
        settings.wechat_callback_secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


@pytest.mark.asyncio
async def test_auth_send_code_and_login(client):
    send_resp = await client.post("/api/v1/auth/send-code", json={"phone": "13800138001"})
    assert send_resp.status_code == 200
    assert send_resp.json()["code"] == 0
    assert send_resp.json()["data"]["success"] is True

    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"phone": "13800138001", "code": "123456"},
    )
    assert login_resp.status_code == 200
    body = login_resp.json()
    assert body["code"] == 0
    assert body["data"]["token"].startswith("mock-")
    assert body["data"]["role"] == "user"


@pytest.mark.asyncio
async def test_order_create_and_query(client):
    create_resp = await client.post(
        "/api/v1/orders",
        json={
            "user_id": "u-test-1",
            "order_type": "pickup",
            "pickup_address": "北门驿站",
            "delivery_address": "1号宿舍楼",
            "contact_phone": "13800138000",
            "remark": "测试订单",
            "amount_cents": 1200,
        },
    )
    assert create_resp.status_code == 200
    create_body = create_resp.json()
    assert create_body["code"] == 0
    order_id = create_body["data"]["id"]
    assert create_body["data"]["status"] == "pending_pay"

    list_resp = await client.get("/api/v1/orders", params={"user_id": "u-test-1"})
    assert list_resp.status_code == 200
    assert list_resp.json()["code"] == 0
    assert len(list_resp.json()["data"]) >= 1

    detail_resp = await client.get(f"/api/v1/orders/{order_id}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["code"] == 0
    assert detail_resp.json()["data"]["id"] == order_id


@pytest.mark.asyncio
async def test_payment_callback_success_flow(client):
    order_resp = await client.post(
        "/api/v1/orders",
        json={
            "user_id": "u-test-1",
            "order_type": "buy",
            "pickup_address": "一食堂",
            "delivery_address": "图书馆",
            "contact_phone": "13800138000",
            "remark": "支付联调",
            "amount_cents": 3000,
        },
    )
    order_id = order_resp.json()["data"]["id"]

    create_pay_resp = await client.post("/api/v1/payments/create", json={"order_id": order_id})
    assert create_pay_resp.status_code == 200
    assert create_pay_resp.json()["code"] == 0

    ts = int(time.time())
    nonce = "nonce-test"
    signature = sign_callback(order_id, "wx_txn_test_001", "success", ts, nonce)
    callback_resp = await client.post(
        "/api/v1/payments/wechat/callback",
        json={
            "order_id": order_id,
            "provider_txn_id": "wx_txn_test_001",
            "status": "success",
            "timestamp": ts,
            "nonce": nonce,
            "signature": signature,
        },
    )
    assert callback_resp.status_code == 200
    assert callback_resp.json()["code"] == 0

    pay_status_resp = await client.get(f"/api/v1/payments/{order_id}/status")
    assert pay_status_resp.status_code == 200
    assert pay_status_resp.json()["data"]["status"] == "success"

    order_detail_resp = await client.get(f"/api/v1/orders/{order_id}")
    assert order_detail_resp.status_code == 200
    assert order_detail_resp.json()["data"]["status"] == "pending_take"

