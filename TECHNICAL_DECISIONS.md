# Technical Decisions

## Backend Framework
- **Framework**: FastAPI
- **Version**: Latest stable
- **Reasoning**:
  - High performance (async support)
  - Automatic API documentation with Swagger UI and ReDoc
  - Type hints and data validation with Pydantic
  - Easy to test and maintain

## Database
- **Database**: SQLite (Development), PostgreSQL (Production)
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Connection Pooling**: SQLAlchemy's built-in pool

## Authentication & Authorization
- **Authentication**: OAuth2 with JWT
- **Password Hashing**: Passlib (bcrypt)
- **Token Management**: Python-JOSE
- **Social Auth**: Support for Google, GitHub (future)
- **Session Management**: Stateless JWT tokens

## API Design
- **Documentation**: OpenAPI (via FastAPI)
- **Versioning**: URL path versioning (e.g., /api/v1/)
- **Response Format**: JSON
- **Error Handling**: Standardized error responses
- **Rate Limiting**: To be implemented
- **CORS**: Enabled for frontend domains

## Testing
- **Framework**: pytest
- **Coverage**: pytest-cov
- **Test Structure**:
  - Unit tests for models and utilities
  - Integration tests for API endpoints
  - E2E tests for critical user flows
- **Mocking**: unittest.mock and pytest-mock

## Development & Deployment
- **Environment Management**: python-dotenv
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Deployment Target**: AWS (ECS/EKS)
- **Infrastructure as Code**: Terraform (future)

## Code Quality
- **Linting**: flake8, black, isort
- **Type Checking**: mypy
- **Security**: bandit, safety
- **Pre-commit Hooks**: Pre-commit framework

## Dependencies
- **Core**:
  - fastapi
  - uvicorn
  - sqlalchemy
  - pydantic
  - python-jose
  - passlib
  - python-multipart
  - python-dotenv
  - alembic
  - pytest
  - httpx

## Project Structure
```
server/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app instance
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic models
│   ├── api/              # API routes
│   │   ├── __init__.py
│   │   ├── v1/           # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── auth.py   # Auth endpoints
│   │   │   └── users.py  # User management
│   └── core/             # Core functionality
│       ├── security.py   # Auth utils
│       └── config.py     # Settings
├── tests/                # Test files
│   ├── conftest.py
│   ├── test_*.py
├── alembic/              # Database migrations
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
└── .env.example
```

## Important Notes
1. All environment variables must be defined in `.env` and documented in `.env.example`
2. Database migrations must be created for all model changes
3. API endpoints must be documented using FastAPI's docstrings
4. Tests must be written for all new features
5. Code must pass all linters and type checks before committing
