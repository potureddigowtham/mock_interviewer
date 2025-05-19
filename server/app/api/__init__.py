"""API package."""
from fastapi import APIRouter

from .v1.api import api_router as v1_router

# Create main API router
api_router = APIRouter()

# Include API version routers
api_router.include_router(v1_router, prefix="/v1")
