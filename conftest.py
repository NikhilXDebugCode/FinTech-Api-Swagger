"""
Shared test fixtures.

Provides:
    - An in-memory SQLite database (no leftover files)
    - A FastAPI TestClient
    - Pre-seeded admin, analyst, and viewer users with JWT tokens
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.models.user import User, UserRole
from app.services.auth_service import create_access_token, hash_password

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def db():
    """Create fresh tables for every test, then tear them down."""
    Base.metadata.create_all(bind=engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """TestClient with the DB session override."""

    def _override():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Helper to create users and tokens ────────────────────────

def _make_user(db, username, email, role):
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password("Test@123"),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(
        {"user_id": user.id, "role": role.value}
    )
    return user, token


@pytest.fixture
def admin_user(db):
    return _make_user(db, "admin", "admin@test.com", UserRole.ADMIN)


@pytest.fixture
def analyst_user(db):
    return _make_user(db, "analyst", "analyst@test.com", UserRole.ANALYST)


@pytest.fixture
def viewer_user(db):
    return _make_user(db, "viewer", "viewer@test.com", UserRole.VIEWER)


def auth_header(token: str) -> dict:
    """Return an Authorization header dict."""
    return {"Authorization": f"Bearer {token}"}
