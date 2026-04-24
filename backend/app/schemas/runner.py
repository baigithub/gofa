from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RunnerOrderItem(BaseModel):
    id: str
    user_id: str
    runner_id: Optional[str]
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


class RunnerActionResponse(BaseModel):
    success: bool = True


class RunnerVerificationItem(BaseModel):
    id: str
    user_id: str
    student_no: Optional[str]
    credential_images: list[str] = Field(default_factory=list)
    verification_status: str
    rejection_reason: Optional[str]
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SubmitRunnerVerificationRequest(BaseModel):
    user_id: str
    student_no: Optional[str] = None
    credential_images: list[str] = Field(default_factory=list)


class UploadCredentialImageResponse(BaseModel):
    success: bool = True
    path: str
    url: str
    filename: str


class ReviewRunnerVerificationRequest(BaseModel):
    admin_user_id: str
    approve: bool
    rejection_reason: Optional[str] = None


class ChatMessageItem(BaseModel):
    id: str
    order_id: str
    sender_user_id: str
    sender_role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SendChatMessageRequest(BaseModel):
    sender_user_id: str
    sender_role: str = Field(pattern="^(user|runner|admin)$")
    content: str = Field(min_length=1, max_length=500)


class ReviewRequest(BaseModel):
    user_id: str
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=500)


class ReviewItem(BaseModel):
    order_id: str
    user_id: str
    runner_id: Optional[str]
    rating: int
    comment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

