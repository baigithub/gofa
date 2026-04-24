from .auth import router as auth_router
from .admin import router as admin_router
from .orders import router as orders_router
from .payments import router as payments_router
from .runner import router as runner_router

__all__ = ["auth_router", "admin_router", "orders_router", "payments_router", "runner_router"]

