"""Main application package."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import models to ensure they are registered with SQLAlchemy
from .models.user import User  # noqa
from .models.base import Base  # noqa

# Import the database session and settings
from .db.base import SessionLocal, engine
from .core.config import settings

# Import API routers
from .api.v1 import api_router as v1_router

def create_tables():
    """Create database tables."""
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    logger.info("Creating FastAPI application...")
    
    # Create tables when the app starts
    create_tables()
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Backend API for the AI Interviewer application",
        version="0.1.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(
        v1_router,
        prefix="/api/v1",
        tags=["v1"]
    )

    # Database session dependency
    @app.middleware("http")
    async def db_session_middleware(request, call_next):
        request.state.db = SessionLocal()
        try:
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response

    return app

# Create the FastAPI application
app = create_app()
