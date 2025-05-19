"""Verify database connection and table creation."""
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.db.base import SessionLocal, engine
from app.models.base import Base

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_database():
    """Check database connection and tables."""
    logger.info("Verifying database setup...")
    
    # Create a new session
    db = SessionLocal()
    
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
        
        # Check tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"📊 Available tables: {tables}")
        
        if 'users' in tables:
            logger.info("✅ Users table exists")
            
            # Check if admin user exists
            from app.models.user import User, UserRole
            admin = db.query(User).filter(User.role == UserRole.ADMIN.value).first()
            if admin:
                logger.info(f"✅ Admin user found: {admin.email}")
            else:
                logger.warning("⚠️  No admin user found")
        else:
            logger.error("❌ Users table does not exist")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Error verifying database: {e}", exc_info=True)
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if check_database():
        logger.info("✅ Database verification completed successfully")
    else:
        logger.error("❌ Database verification failed")
        sys.exit(1)
