from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateOrderRequest(BaseModel):
    user_id: str
    order_type: str = Field(pattern="^(pickup|buy|errand)$")
    pickup_address: Optional[str] = None
    delivery_address: Optional[str] = None
    contact_phone: str = Field(min_length=11, max_length=20)
    remark: Optional[str] = None
    amount_cents: int = Field(ge=0)


class OrderResponse(BaseModel):
    id: str
    user_id: str
    order_type: str
    status: str
    pickup_address: Optional[str]
    delivery_address: Optional[str]
    contact_phone: str
    remark: Optional[str]
    amount_cents: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CancelOrderResponse(BaseModel):
    success: bool = True

