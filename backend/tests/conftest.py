import hashlib
import hmac
from typing import Generator

import pytest
import pytest_asyncio
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.app.core.config import settings
from backend.app.core.db import get_db
from backend.app.main import app
from backend.app.models import Base, User


@pytest.fixture()
def test_db() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///./test_gofer.db", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    db.add(User(id="u-test-1", phone="13800138000"))
    db.commit()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest_asyncio.fixture()
async def client(test_db: Session) -> Generator[httpx.AsyncClient, None, None]:
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    settings.wechat_callback_secret = "gofer-wechat-dev-secret"
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c
    app.dependency_overrides.clear()


def sign_callback(order_id: str, provider_txn_id: str, status: str, timestamp: int, nonce: str) -> str:
    message = f"{order_id}|{provider_txn_id}|{status}|{timestamp}|{nonce}"
    return hmac.new(
        settings.wechat_callback_secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

