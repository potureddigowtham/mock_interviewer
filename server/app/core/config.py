"""Application configuration settings."""
import os
import json
from pathlib import Path
from typing import List, Optional, Any, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables manually
env_path = Path(__file__).parent.parent.parent.parent / ".env"

if not env_path.exists():
    raise FileNotFoundError(f"Cannot find .env file at {env_path}")

# Load environment variables with dotenv
from dotenv import load_dotenv
load_dotenv(dotenv_path=env_path)
logger.info(f"Loaded environment variables from {env_path}")

# Verify SECRET_KEY is present
if not os.getenv("SECRET_KEY"):
    raise ValueError("SECRET_KEY environment variable is not set in .env file")

# Define settings class with manually loaded environment variables
class Settings:
    """Application settings."""
    
    # Project metadata
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "AI Interviewer API")
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() in ("true", "1", "t")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")  # Will raise error if not set above
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 days
    
    # CORS
    BACKEND_CORS_ORIGINS_STR: str = os.getenv("BACKEND_CORS_ORIGINS", '[]')
    BACKEND_CORS_ORIGINS: List[str] = json.loads(BACKEND_CORS_ORIGINS_STR) \
        if BACKEND_CORS_ORIGINS_STR else ["http://localhost:3000", "http://localhost:8000"]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_interviewer.db")
    
    # First admin user
    FIRST_SUPERUSER_EMAIL: str = os.getenv("FIRST_SUPERUSER_EMAIL", "admin@example.com")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "changethis")
    
    # OpenAI API
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

# Create settings instance and expose environmental variables for debugging
settings = Settings()
logger.info(f"Environment variables loaded:")
logger.info(f"PROJECT_NAME: {settings.PROJECT_NAME}")
logger.info(f"ENVIRONMENT: {settings.ENVIRONMENT}")
logger.info(f"SECRET_KEY set: {bool(settings.SECRET_KEY)}")
logger.info(f"DATABASE_URL: {settings.DATABASE_URL}")
logger.info(f"BACKEND_CORS_ORIGINS: {settings.BACKEND_CORS_ORIGINS}")