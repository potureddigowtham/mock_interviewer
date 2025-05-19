"""Initialize the database with default data."""
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.base import Base
from app.core.security import get_password_hash

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_tables() -> None:
    """Create database tables if they don't exist."""
    logger.info("Creating database tables...")
    
    try:
        # Import all models to ensure they are registered with SQLAlchemy
        from app.models.user import User  # noqa
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Available tables: {tables}")
        
        if 'users' not in tables:
            raise RuntimeError("Users table was not created successfully")
            
    except Exception as e:
        logger.error(f"Error creating tables: {e}", exc_info=True)
        raise

def init_db() -> None:
    """Initialize the database with default data."""
    logger.info("Initializing database...")
    
    # Create tables first
    create_tables()
    
    # Create a new session
    db = SessionLocal()
    
    try:
        # Verify database connection
        db.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        
        # Check if admin user already exists
        logger.info(f"Checking for admin user with email: {settings.FIRST_SUPERUSER_EMAIL}")
        admin = db.query(User).filter(User.email == settings.FIRST_SUPERUSER_EMAIL).first()
        
        if admin is None:
            logger.info("Creating initial admin user...")
            admin = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                username="admin",
                full_name="Admin User",
                role=UserRole.ADMIN.value,
                is_active=True
            )
            admin.hashed_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
            
            db.add(admin)
            db.commit()
            db.refresh(admin)
            logger.info(f"Admin user created successfully with ID: {admin.id}")
        else:
            logger.info(f"Admin user already exists with ID: {admin.id}")
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()
        logger.info("Database initialization complete")

if __name__ == "__main__":
    logger.info("Initializing database...")
    try:
        init_db()
        logger.info("✅ Database initialization completed successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    logger.info("Database initialization complete.")
