from __future__ import annotations

from datetime import datetime
import json

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from ..models import Order, Role, RunnerProfile, User
from .auth_service import reset_login_code


def require_admin(db: Session, admin_user_id: str) -> User:
    admin = db.execute(select(User).where(User.id == admin_user_id)).scalar_one_or_none()
    if admin is None:
        raise ValueError("管理员不存在")
    if not admin.is_enabled:
        raise ValueError("管理员账号已禁用")
    if admin.role != "admin":
        raise ValueError("无管理员权限")
    return admin


def ensure_builtin_roles(db: Session) -> None:
    builtin = [
        ("user", "普通用户", "普通下单用户"),
        ("runner", "跑腿员", "可接单和配送"),
        ("admin", "管理员", "拥有后台管理权限"),
    ]
    existing = {r.code: r for r in db.execute(select(Role)).scalars().all()}
    created = False
    for code, name, description in builtin:
        if code in existing:
            continue
        db.add(Role(code=code, name=name, description=description, is_enabled=True))
        created = True
    if created:
        db.commit()


def list_users(db: Session) -> list[User]:
    stmt = select(User).order_by(User.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def set_user_role(db: Session, user_id: str, role: str) -> bool:
    ensure_builtin_roles(db)
    role_obj = db.execute(select(Role).where(Role.code == role)).scalar_one_or_none()
    if role_obj is None:
        raise ValueError("角色不存在")
    if not role_obj.is_enabled:
        raise ValueError("目标角色已禁用")
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise ValueError("用户不存在")
    user.role = role
    db.commit()
    return True


def set_user_enabled(db: Session, user_id: str, is_enabled: bool) -> bool:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise ValueError("用户不存在")
    if user.role == "admin" and not is_enabled:
        admin_count = db.execute(
            select(User).where(User.role == "admin", User.is_enabled.is_(True))
        ).scalars().all()
        if len(admin_count) <= 1 and user.is_enabled:
            raise ValueError("至少保留一个启用中的管理员")
    user.is_enabled = is_enabled
    db.commit()
    return True


def reset_user_password(db: Session, user_id: str) -> str:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise ValueError("用户不存在")
    temp_password = "123456"
    reset_login_code(user.phone, temp_password)
    return temp_password


def list_roles(db: Session) -> list[Role]:
    ensure_builtin_roles(db)
    return list(db.execute(select(Role).order_by(Role.created_at.asc())).scalars().all())


def create_role(db: Session, code: str, name: str, description: str | None) -> Role:
    ensure_builtin_roles(db)
    existing = db.execute(select(Role).where(Role.code == code)).scalar_one_or_none()
    if existing is not None:
        raise ValueError("角色编码已存在")
    role = Role(code=code, name=name, description=description, is_enabled=True)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, role_id: str, name: str, description: str | None) -> Role:
    role = db.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
    if role is None:
        raise ValueError("角色不存在")
    role.name = name
    role.description = description
    db.commit()
    db.refresh(role)
    return role


def set_role_enabled(db: Session, role_id: str, is_enabled: bool) -> Role:
    role = db.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
    if role is None:
        raise ValueError("角色不存在")
    if role.code == "admin" and not is_enabled:
        raise ValueError("管理员角色不允许禁用")
    role.is_enabled = is_enabled
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role_id: str) -> bool:
    role = db.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
    if role is None:
        raise ValueError("角色不存在")
    if role.code in {"user", "runner", "admin"}:
        raise ValueError("内置角色不允许删除")
    in_use = db.execute(select(User).where(User.role == role.code)).scalars().first()
    if in_use is not None:
        raise ValueError("该角色仍有用户使用，无法删除")
    db.delete(role)
    db.commit()
    return True


def list_admin_orders(db: Session) -> list[dict]:
    initiator_user = aliased(User)
    runner_user = aliased(User)
    stmt = (
        select(Order, initiator_user.phone, runner_user.phone)
        .join(initiator_user, Order.user_id == initiator_user.id)
        .outerjoin(RunnerProfile, Order.runner_id == RunnerProfile.id)
        .outerjoin(runner_user, RunnerProfile.user_id == runner_user.id)
        .order_by(Order.created_at.desc())
    )
    rows = db.execute(stmt).all()

    result: list[dict] = []
    for order, initiator_phone, runner_phone in rows:
        content = order.remark or f"{order.pickup_address or '-'} -> {order.delivery_address or '-'}"
        result.append(
            {
                "order_id": order.id,
                "order_content": content,
                "initiator": initiator_phone,
                "runner": runner_phone or "未接单",
                "status": order.status,
                "created_at": order.created_at.isoformat(),
                "completed_at": order.completed_at.isoformat() if order.completed_at else None,
                "required_completed_at": (
                    order.required_completed_at.isoformat() if order.required_completed_at else None
                ),
            }
        )
    return result
+
+
+def get_runner_dashboard_stats(db: Session, runner_user_id: str) -> dict:
+    runner = db.execute(select(RunnerProfile).where(RunnerProfile.user_id == runner_user_id)).scalar_one_or_none()
+    if runner is None:
+        raise ValueError("跑腿员不存在")
+
+    available_orders = db.execute(select(Order).where(Order.status == "pending_take")).scalars().all()
+    today = datetime.utcnow().date()
+    start = datetime(today.year, today.month, today.day)
+    today_completed = db.execute(
+        select(Order).where(Order.completed_at.is_not(None), Order.completed_at >= start, Order.runner_id == runner.id)
+    ).scalars().all()
+    today_earnings_cents = sum(order.amount_cents for order in today_completed)
+    return {
+        "today_earnings_cents": today_earnings_cents,
+        "available_order_count": len(available_orders),
+        "verification_status": runner.verification_status,
+        "is_verified": runner.is_verified,
+        "rejection_reason": runner.rejection_reason,
+    }


def _serialize_images(images: list[str] | None) -> str:
    return json.dumps([img for img in (images or []) if isinstance(img, str)], ensure_ascii=False)


def list_runner_verifications(db: Session) -> list[RunnerProfile]:
    stmt = select(RunnerProfile).order_by(RunnerProfile.updated_at.desc())
    return list(db.execute(stmt).scalars().all())


def submit_runner_verification(
    db: Session,
    user_id: str,
    student_no: str | None,
    credential_images: list[str],
) -> RunnerProfile:
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise ValueError("用户不存在")
    if user.role != "runner":
        user.role = "runner"

    profile = db.execute(select(RunnerProfile).where(RunnerProfile.user_id == user_id)).scalar_one_or_none()
    if profile is None:
        profile = RunnerProfile(user_id=user_id)
        db.add(profile)

    if profile.verification_status == "pending":
        raise ValueError("认证审核中，请勿重复提交")

    profile.student_no = student_no
    profile.credential_images = _serialize_images(credential_images)
    profile.verification_status = "pending"
    profile.rejection_reason = None
    profile.reviewed_by = None
    profile.reviewed_at = None
    profile.is_verified = False
    user.role = "runner"
    db.commit()
    db.refresh(profile)
    return profile


def review_runner_verification(
    db: Session,
    profile_id: str,
    admin_user_id: str,
    approve: bool,
    rejection_reason: str | None,
) -> RunnerProfile:
    profile = db.execute(select(RunnerProfile).where(RunnerProfile.id == profile_id)).scalar_one_or_none()
    if profile is None:
        raise ValueError("认证记录不存在")
    admin = require_admin(db, admin_user_id)
    profile.reviewed_by = admin.id
    profile.reviewed_at = datetime.utcnow()
    if approve:
        profile.verification_status = "approved"
        profile.rejection_reason = None
        profile.is_verified = True
    else:
        profile.verification_status = "rejected"
        profile.rejection_reason = rejection_reason or "资料不符合要求"
        profile.is_verified = False
    db.commit()
    db.refresh(profile)
    return profile

