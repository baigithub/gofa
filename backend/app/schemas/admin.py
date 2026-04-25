from typing import Optional

from pydantic import BaseModel, Field


class UserItem(BaseModel):
    id: str
    phone: str
    nickname: Optional[str]
    role: str
    is_enabled: bool
    created_at: str


class SetUserRoleRequest(BaseModel):
    role: str = Field(pattern="^(user|runner|admin)$")


class SetUserRoleResponse(BaseModel):
    success: bool = True


class ResetPasswordResponse(BaseModel):
    success: bool = True
    temp_password: str


class AdminOrderItem(BaseModel):
    order_id: str
    order_content: str
    initiator: str
    runner: str
    status: str
    created_at: str
    completed_at: Optional[str]
    required_completed_at: Optional[str]


class SetUserEnabledRequest(BaseModel):
    is_enabled: bool


class RoleItem(BaseModel):
    id: str
    code: str
    name: str
    description: Optional[str]
    is_enabled: bool
    created_at: str
    updated_at: str


class CreateRoleRequest(BaseModel):
    code: str = Field(min_length=2, max_length=20, pattern="^[a-z][a-z0-9_]*$")
    name: str = Field(min_length=1, max_length=50)
    description: Optional[str] = None


class UpdateRoleRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: Optional[str] = None


class SetRoleEnabledRequest(BaseModel):
    is_enabled: bool

