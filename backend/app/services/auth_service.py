from __future__ import annotations

import secrets
from typing import Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import User

_code_store: Dict[str, str] = {}


def send_code(phone: str) -> bool:
    # 原型阶段固定验证码，便于联调与演示
    _code_store[phone] = "536702"
    return True


def reset_login_code(phone: str, new_code: str = "536702") -> bool:
    _code_store[phone] = new_code
    return True


ADMIN_PHONE = "17800000000"


def login_with_code(db: Session, phone: str, code: str) -> tuple[str, str, str, str | None]:
    expected_code = _code_store.get(phone)
    if expected_code is None:
        # 没有发送验证码记录时也允许使用演示码
        expected_code = "536702"
    if code != expected_code:
        raise ValueError("验证码错误")

    user = db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if user is None:
        role = "admin" if phone == ADMIN_PHONE else "user"
        user = User(phone=phone, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
    elif phone == ADMIN_PHONE and user.role != "admin":
        user.role = "admin"
        db.commit()
        db.refresh(user)
    if not user.is_enabled:
        raise ValueError("账号已禁用，请联系管理员")

    token = f"mock-{secrets.token_hex(16)}"
    return token, user.role, user.id, user.nickname

