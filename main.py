"""
FastAPI application entry point.

Registers routers, creates DB tables on startup, and configures
global exception handling.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.routers import analytics, auth, transactions, users


# ── Lifespan: create tables on startup ───────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all database tables when the application starts."""
    Base.metadata.create_all(bind=engine)
    yield


# ── App instance ─────────────────────────────────────────────

app = FastAPI(
    title="FinTrack API",
    description=(
        "A Python-powered finance tracking system for managing "
        "transactions, generating analytics, and enforcing role-based "
        "access control."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── Register routers ────────────────────────────────────────

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(analytics.router)


# ── Global exception handler ────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all for unhandled exceptions; returns a safe 500 response."""
    # Re-raise known HTTP exceptions so FastAPI handles them normally
    if isinstance(exc, HTTPException):
        raise exc
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again later."
        },
    )


# ── Health check ─────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    """Health-check endpoint."""
    return {
        "status": "healthy",
        "service": "FinTrack API",
        "version": "1.0.0",
        "docs": "/docs",
    }
