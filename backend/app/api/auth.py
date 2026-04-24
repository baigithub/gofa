from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from ..core import error_codes
from ..core.db import get_db
from ..core.exceptions import ApiException
from ..core.response import success
from ..schemas.auth import LoginRequest, LoginResponse, SendCodeRequest, SendCodeResponse
from ..services.auth_service import login_with_code, send_code

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/send-code")
def send_sms_code(
    payload: SendCodeRequest = Body(
        ...,
        examples={
            "default": {
                "summary": "发送验证码示例",
                "value": {"phone": "13800138000"},
            }
        },
    )
):
    ok = send_code(payload.phone)
    return success(SendCodeResponse(success=ok).model_dump())


@router.post("/login")
def login(
    payload: LoginRequest = Body(
        ...,
        examples={
            "default": {
                "summary": "登录示例",
                "value": {"phone": "13800138000", "code": "123456"},
            }
        },
    ),
    db: Session = Depends(get_db),
):
    try:
        token, role, user_id = login_with_code(db, payload.phone, payload.code)
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(LoginResponse(token=token, role=role, user_id=user_id).model_dump())

