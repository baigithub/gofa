from typing import Any

from . import error_codes


def success(data: Any = None, message: str = "ok") -> dict[str, Any]:
    return {
        "code": error_codes.SUCCESS,
        "message": message,
        "data": data,
    }


def error(code: int, message: str, data: Any = None) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "data": data,
    }

