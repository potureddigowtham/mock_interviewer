"""API v1 router configuration."""
from fastapi import APIRouter

from .endpoints import auth, users

api_router = APIRouter()

# Include API endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
