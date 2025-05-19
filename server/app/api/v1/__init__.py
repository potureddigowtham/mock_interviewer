"""API v1 router."""
from fastapi import APIRouter
from app.api.health import router as health_router

# Import API routers
from .api import api_router as v1_endpoints_router

# Create main router
api_router = APIRouter()

# Include health check endpoint
api_router.include_router(health_router, tags=["health"])

# Include authentication and user endpoints
api_router.include_router(v1_endpoints_router)
