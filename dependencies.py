"""
Shared FastAPI dependencies.

    - ``get_db``            – yields a SQLAlchemy session per request
    - ``get_current_user``  – decodes the JWT and returns the User
    - ``require_roles``     – factory that returns a dependency enforcing
                              one or more allowed roles
"""

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.services.auth_service import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ── Database session ─────────────────────────────────────────

def get_db():
    """Yield a DB session and ensure it is closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Current user ─────────────────────────────────────────────

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> User:
    """Decode the JWT and return the corresponding User row."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: Optional[int] = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception

    return user


# ── Role enforcement ─────────────────────────────────────────

def require_roles(*allowed: UserRole):
    """
    Return a dependency that raises 403 if the current user's role
    is not in *allowed*.

    Usage::

        @router.get("/admin-only", dependencies=[Depends(require_roles(UserRole.ADMIN))])
    """

    def _checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return _checker
