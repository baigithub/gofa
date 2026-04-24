from pydantic import BaseModel, Field


class SendCodeRequest(BaseModel):
    phone: str = Field(min_length=11, max_length=20)


class SendCodeResponse(BaseModel):
    success: bool = True


class LoginRequest(BaseModel):
    phone: str = Field(min_length=11, max_length=20)
    code: str = Field(min_length=4, max_length=8)


class LoginResponse(BaseModel):
    token: str
    role: str
    user_id: str

