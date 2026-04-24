from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CreatePaymentRequest(BaseModel):
    order_id: str


class PaymentResponse(BaseModel):
    id: str
    order_id: str
    provider: str
    status: str
    amount_cents: int
    provider_txn_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentStatusResponse(BaseModel):
    order_id: str
    status: str


class WechatCallbackRequest(BaseModel):
    order_id: str
    provider_txn_id: str = Field(min_length=1, max_length=64)
    status: str = Field(pattern="^(success|failed)$")
    timestamp: int
    nonce: str = Field(min_length=1, max_length=64)
    signature: str = Field(min_length=1, max_length=128)


class CallbackResponse(BaseModel):
    success: bool = True

