import os
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core import error_codes
from ..core.db import get_db
from ..core.exceptions import ApiException
from ..core.response import success
from ..models import User
from ..schemas.runner import (
    ChatMessageItem,
    ReviewItem,
    ReviewRequest,
    RunnerActionResponse,
    RunnerOrderItem,
    SendChatMessageRequest,
    SubmitRunnerVerificationRequest,
    UploadCredentialImageResponse,
)
from ..services.admin_service import get_runner_dashboard_stats, submit_runner_verification
from ..services.runner_service import (
    accept_order,
    delivered_order,
    get_review,
    list_hall_orders,
    list_order_chats,
    send_order_chat,
    submit_review,
)

router = APIRouter(prefix="/api/v1/runner", tags=["runner"])
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploadfile"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/credential-image")
async def upload_credential_image_api(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        raise ApiException(error_codes.BAD_REQUEST, "仅支持图片文件", status_code=400)

    safe_name = f"{uuid4().hex}{suffix}"
    target = UPLOAD_DIR / safe_name
    content = await file.read()
    target.write_bytes(content)
    url = f"/uploadfile/{safe_name}"
    return success(
        UploadCredentialImageResponse(
            path=str(target),
            url=url,
            filename=file.filename or safe_name,
        ).model_dump()
    )


@router.post("/verification/submit")
def submit_runner_verification_api(payload: SubmitRunnerVerificationRequest, db: Session = Depends(get_db)):
    try:
        user = db.execute(select(User).where(User.phone == payload.user_id)).scalar_one_or_none()
        user_id = user.id if user else payload.user_id
        item = submit_runner_verification(
            db,
            user_id=user_id,
            student_no=payload.student_no,
            credential_images=payload.credential_images,
        )
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success({"success": True, "runner_profile_id": item.id})


@router.get("/stats")
def runner_dashboard_stats_api(runner_user_id: str = Query(...), db: Session = Depends(get_db)):
    try:
        stats = get_runner_dashboard_stats(db, runner_user_id=runner_user_id)
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(stats)


@router.get("/orders/hall")
def hall_orders_api(db: Session = Depends(get_db)):
    items = list_hall_orders(db)
    data = [RunnerOrderItem.model_validate(item).model_dump() for item in items]
    return success(data)


@router.post("/orders/{order_id}/accept")
def accept_order_api(
    order_id: str,
    runner_id: str = Query(..., description="跑腿员ID"),
    db: Session = Depends(get_db),
):
    try:
        accept_order(db, order_id=order_id, runner_id=runner_id)
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(RunnerActionResponse(success=True).model_dump())


@router.post("/orders/{order_id}/delivered")
def delivered_order_api(
    order_id: str,
    runner_id: str = Query(..., description="跑腿员ID"),
    db: Session = Depends(get_db),
):
    try:
        delivered_order(db, order_id=order_id, runner_id=runner_id)
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(RunnerActionResponse(success=True).model_dump())


@router.get("/orders/{order_id}/chats")
def list_order_chats_api(order_id: str, db: Session = Depends(get_db)):
    items = list_order_chats(db, order_id=order_id)
    data = [ChatMessageItem.model_validate(item).model_dump() for item in items]
    return success(data)


@router.post("/orders/{order_id}/chats")
def send_order_chat_api(order_id: str, payload: SendChatMessageRequest, db: Session = Depends(get_db)):
    try:
        item = send_order_chat(
            db,
            order_id=order_id,
            sender_user_id=payload.sender_user_id,
            sender_role=payload.sender_role,
            content=payload.content,
        )
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(ChatMessageItem.model_validate(item).model_dump())


@router.post("/orders/{order_id}/review")
def submit_review_api(order_id: str, payload: ReviewRequest, db: Session = Depends(get_db)):
    try:
        review = submit_review(
            db,
            order_id=order_id,
            user_id=payload.user_id,
            rating=payload.rating,
            comment=payload.comment,
        )
    except ValueError as exc:
        raise ApiException(error_codes.BAD_REQUEST, str(exc), status_code=400) from exc
    return success(ReviewItem.model_validate(review).model_dump())


@router.get("/orders/{order_id}/review")
def get_review_api(order_id: str, db: Session = Depends(get_db)):
    review = get_review(db, order_id=order_id)
    if review is None:
        return success(None)
    return success(ReviewItem.model_validate(review).model_dump())
