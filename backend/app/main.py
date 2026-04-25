import logging
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text

from .api import admin_router, auth_router, orders_router, payments_router, runner_router
from .core import error_codes
from .core.db import engine
from .core.exceptions import ApiException
from .core.logging_config import setup_logging
from .core.response import error, success

setup_logging()
logger = logging.getLogger("gofer.api")

app = FastAPI(
    title="Gofer Campus API",
    version="0.1.0",
    description="校园跑腿系统后端接口文档（FastAPI + MySQL）",
    openapi_tags=[
        {"name": "auth", "description": "认证相关接口"},
        {"name": "admin", "description": "管理员接口（分配角色等）"},
        {"name": "orders", "description": "订单相关接口"},
        {"name": "payments", "description": "支付相关接口（微信最小方案）"},
        {"name": "runner", "description": "跑腿员相关接口"},
    ],
)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(runner_router)
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploadfile"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploadfile", StaticFiles(directory=str(UPLOAD_DIR)), name="uploadfile")


@app.middleware("http")
async def request_trace_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start = time.perf_counter()

    logger.info("request.start id=%s method=%s path=%s", request_id, request.method, request.url.path)
    response = await call_next(request)

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request.end id=%s method=%s path=%s status=%s cost_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.get("/health")
def health():
    return success({"ok": True})


@app.get("/db/ping")
def db_ping():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return success({"ok": True})


@app.exception_handler(ApiException)
async def handle_api_exception(_: Request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error(exc.code, exc.message),
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error(error_codes.VALIDATION_ERROR, "请求参数校验失败", data=exc.errors()),
    )


@app.exception_handler(HTTPException)
async def handle_http_exception(_: Request, exc: HTTPException):
    code = error_codes.BAD_REQUEST
    if exc.status_code == 401:
        code = error_codes.UNAUTHORIZED
    elif exc.status_code == 403:
        code = error_codes.FORBIDDEN
    elif exc.status_code == 404:
        code = error_codes.NOT_FOUND
    return JSONResponse(status_code=exc.status_code, content=error(code, str(exc.detail)))


@app.exception_handler(Exception)
async def handle_unexpected_error(_: Request, __: Exception):
    return JSONResponse(
        status_code=500,
        content=error(error_codes.INTERNAL_ERROR, "服务器内部错误"),
    )

