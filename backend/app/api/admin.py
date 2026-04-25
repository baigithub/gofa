import json

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from ..core import error_codes
from ..core.db import get_db
from ..core.exceptions import ApiException
from ..core.response import success
from ..schemas.admin import (
    AdminOrderItem,
    CreateRoleRequest,
    ResetPasswordResponse,
    RoleItem,
    SetRoleEnabledRequest,
    SetUserEnabledRequest,
    SetUserRoleRequest,
    SetUserRoleResponse,
    UpdateRoleRequest,
    UserItem,
)
from ..schemas.runner import ReviewRunnerVerificationRequest, RunnerVerificationItem, SubmitRunnerVerificationRequest
from ..services.admin_service import (
    create_role,
    delete_role,
    list_admin_orders,
    list_roles,
    list_runner_verifications,
    list_users,
    require_admin,
    reset_user_password,
    review_runner_verification,
    set_role_enabled,
    set_user_enabled,
    set_user_role,
    update_role,
    submit_runner_verification,
)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/users")
def list_users_api(admin_user_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        require_admin(db, admin_user_id)
        users = list_users(db)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc

    data = [
        UserItem(
            id=u.id,
            phone=u.phone,
            role=u.role,
            is_enabled=u.is_enabled,
            created_at=u.created_at.isoformat(),
        ).model_dump()
        for u in users
    ]
    return success(data)


@router.post("/users/{user_id}/role")
def set_user_role_api(
    user_id: str,
    payload: SetUserRoleRequest = Body(...),
    admin_user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        require_admin(db, admin_user_id)
        set_user_role(db, user_id=user_id, role=payload.role)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc
    return success(SetUserRoleResponse(success=True).model_dump())


@router.post("/users/{user_id}/reset-password")
def reset_password_api(
    user_id: str,
    admin_user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        require_admin(db, admin_user_id)
        temp_password = reset_user_password(db, user_id=user_id)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc
    return success(ResetPasswordResponse(success=True, temp_password=temp_password).model_dump())


@router.post("/users/{user_id}/enabled")
def set_user_enabled_api(
    user_id: str,
    payload: SetUserEnabledRequest = Body(...),
    admin_user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        require_admin(db, admin_user_id)
        set_user_enabled(db, user_id=user_id, is_enabled=payload.is_enabled)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc
    return success({"success": True})


@router.get("/orders")
def admin_orders_api(admin_user_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        require_admin(db, admin_user_id)
        orders = list_admin_orders(db)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc
    data = [AdminOrderItem.model_validate(item).model_dump() for item in orders]
    return success(data)


@router.get("/roles")
def list_roles_api(admin_user_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        require_admin(db, admin_user_id)
        roles = list_roles(db)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc
    data = [RoleItem.model_validate(r).model_dump() for r in roles]
    return success(data)


@router.post("/roles")
def create_role_api(
    payload: CreateRoleRequest = Body(...),
    admin_user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        require_admin(db, admin_user_id)
        role = create_role(db, code=payload.code, name=payload.name, description=payload.description)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc
    return success(RoleItem.model_validate(role).model_dump())


@router.put("/roles/{role_id}")
def update_role_api(
    role_id: str,
    payload: UpdateRoleRequest = Body(...),
    admin_user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        require_admin(db, admin_user_id)
        role = update_role(db, role_id=role_id, name=payload.name, description=payload.description)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc
    return success(RoleItem.model_validate(role).model_dump())


@router.post("/roles/{role_id}/enabled")
def set_role_enabled_api(
    role_id: str,
    payload: SetRoleEnabledRequest = Body(...),
    admin_user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        require_admin(db, admin_user_id)
        role = set_role_enabled(db, role_id=role_id, is_enabled=payload.is_enabled)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc
    return success(RoleItem.model_validate(role).model_dump())


@router.delete("/roles/{role_id}")
def delete_role_api(
    role_id: str,
    admin_user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        require_admin(db, admin_user_id)
        delete_role(db, role_id=role_id)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc
    return success({"success": True})


@router.get("/runner-verifications")
def list_runner_verifications_api(admin_user_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        require_admin(db, admin_user_id)
        items = list_runner_verifications(db)
    except ValueError as exc:
        raise ApiException(error_codes.FORBIDDEN, str(exc), status_code=403) from exc

    data = []
    for item in items:
        images = item.get("credential_images") or []
        if isinstance(images, str):
            try:
                parsed = json.loads(images)
                images = [img for img in parsed if isinstance(img, str)]
            except json.JSONDecodeError:
                images = []
        data.append(
            RunnerVerificationItem(
                id=item["id"],
                user_id=item["user_id"],
                phone=item.get("phone", ""),
                student_no=item.get("student_no"),
                credential_images=images,
                verification_status=item.get("verification_status", "pending"),
                rejection_reason=item.get("rejection_reason"),
                reviewed_by=item.get("reviewed_by"),
                reviewed_at=item.get("reviewed_at"),
                is_verified=item.get("is_verified", False),
                created_at=item["created_at"],
                updated_at=item["updated_at"],
            ).model_dump()
        )
    return success(data)


@router.post("/runner-verifications/submit")
def submit_runner_verification_api(
    payload: SubmitRunnerVerificationRequest = Body(...),
    db: Session = Depends(get_db),
):
    try:
        item = submit_runner_verification(
            db,
            user_id=payload.user_id,
            student_no=payload.student_no,
            credential_images=payload.credential_images,
        )
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(RunnerVerificationItem.model_validate(item).model_dump())


@router.post("/runner-verifications/{profile_id}/review")
def review_runner_verification_api(
    profile_id: str,
    payload: ReviewRunnerVerificationRequest = Body(...),
    db: Session = Depends(get_db),
):
    try:
        item = review_runner_verification(
            db,
            profile_id=profile_id,
            admin_user_id=payload.admin_user_id,
            approve=payload.approve,
            rejection_reason=payload.rejection_reason,
        )
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(
        RunnerVerificationItem(
            id=item.id,
            user_id=item.user_id,
            student_no=item.student_no,
            credential_images=json.loads(item.credential_images or "[]") if item.credential_images else [],
            verification_status=item.verification_status,
            rejection_reason=item.rejection_reason,
            reviewed_by=item.reviewed_by,
            reviewed_at=item.reviewed_at,
            is_verified=item.is_verified,
            created_at=item.created_at,
            updated_at=item.updated_at,
        ).model_dump()
    )

