# Useful FastAPI Codeblock Patterns

> Practical, copy-paste-ready FastAPI patterns for building production-grade Python REST APIs.

---

## 1. Project Structure

```
my-api/
  app/
    __init__.py
    main.py                  # Application factory
    config.py                # Pydantic Settings
    database.py              # Async SQLAlchemy engine + session
    dependencies.py          # Shared Depends() callables
    security.py              # JWT, password hashing
    exceptions.py            # Custom exceptions + handlers
    models/                  # SQLAlchemy ORM models
      __init__.py
      user.py
    schemas/                 # Pydantic v2 request/response schemas
      __init__.py
      user.py
      auth.py
    routers/                 # Endpoints (thin)
      __init__.py
      auth.py
      users.py
      health.py
    services/                # Business logic
      __init__.py
      user_service.py
      auth_service.py
    repositories/            # Data access layer
      __init__.py
      base.py
      user_repository.py
  tests/
    conftest.py
    test_auth.py
    test_users.py
  alembic/
    versions/
  alembic.ini
  requirements.txt
  Dockerfile
  docker-compose.yml
```

---

## 2. Application Factory

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine
from app.routers import api_router
from app.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")
    register_exception_handlers(app)

    return app


app = create_app()
```

---

## 3. Configuration (Pydantic Settings)

```python
# app/config.py
from functools import lru_cache
from typing import List, Optional
from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "MyApp API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")

    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str = Field(..., min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    DATABASE_URL: PostgresDsn
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    REDIS_URL: Optional[str] = None

    LOG_LEVEL: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## 4. Async Database (SQLAlchemy 2.0 + asyncpg)

```python
# app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

## 5. SQLAlchemy Models

```python
# app/models/base.py
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class BaseModel(Base, TimestampMixin):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
```

```python
# app/models/user.py
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String(20), default="user")
```

---

## 6. Pydantic Schemas (v2)

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    name: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserList(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    limit: int
    total_pages: int
```

```python
# app/schemas/auth.py
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
```

---

## 7. Dependencies

```python
# app/dependencies.py
from typing import Annotated, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Type aliases for cleaner signatures
DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentToken = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(
    db: DBSession,
    token: CurrentToken,
) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    repo = UserRepository(db)
    user = await repo.get_by_id(payload.get("sub"))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_role(required_role: str):
    async def role_checker(current_user: CurrentUser) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user
    return Depends(role_checker)


# Usage:
# AdminUser = Annotated[User, require_role("admin")]
```

---

## 8. Security (JWT + Password Hashing)

```python
# app/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

## 9. Repository Pattern (Data Access Layer)

```python
# app/repositories/base.py
from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def list(
        self, skip: int = 0, limit: int = 100, **filters
    ) -> tuple[List[ModelType], int]:
        query = select(self.model)

        for attr, value in filters.items():
            if value is not None:
                column = getattr(self.model, attr, None)
                if column is not None:
                    query = query.where(column == value)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        result = await self.db.execute(query.offset(skip).limit(limit))
        items = list(result.scalars().all())

        return items, total

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def update(self, id: Any, **kwargs) -> Optional[ModelType]:
        instance = await self.get_by_id(id)
        if instance is None:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def delete(self, id: Any) -> bool:
        instance = await self.get_by_id(id)
        if instance is None:
            return False
        await self.db.delete(instance)
        await self.db.flush()
        return True
```

```python
# app/repositories/user_repository.py
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
```

---

## 10. Service Layer (Business Logic)

```python
# app/services/user_service.py
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.security import hash_password


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

        return await self.repo.create(
            email=data.email,
            name=data.name,
            hashed_password=hash_password(data.password),
        )

    async def get_user(self, user_id: str) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def list_users(self, skip: int = 0, limit: int = 100) -> tuple:
        return await self.repo.list(skip=skip, limit=limit)

    async def update_user(self, user_id: str, data: dict) -> User:
        user = await self.repo.update(user_id, **data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def delete_user(self, user_id: str) -> None:
        deleted = await self.repo.delete(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
```

```python
# app/services/auth_service.py
from app.repositories.user_repository import UserRepository
from app.security import verify_password, create_access_token, create_refresh_token, decode_access_token
from app.config import get_settings


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def login(self, email: str, password: str) -> dict:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "access_token": create_access_token({"sub": str(user.id), "role": user.role}),
            "refresh_token": create_refresh_token({"sub": str(user.id)}),
            "token_type": "bearer",
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        payload = decode_access_token(refresh_token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = await self.repo.get_by_id(payload.get("sub"))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "access_token": create_access_token({"sub": str(user.id), "role": user.role}),
            "token_type": "bearer",
        }
```

---

## 11. Routers (Thin Endpoints)

```python
# app/routers/__init__.py
from fastapi import APIRouter
from app.routers import auth, users, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
```

```python
# app/routers/health.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


@router.get("/health/ready")
async def readiness():
    # Add DB connection check
    return {"status": "ready"}
```

```python
# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import DBSession
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.security import hash_password

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, db: DBSession):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.create_user(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: DBSession):
    repo = UserRepository(db)
    service = AuthService(repo)
    return await service.login(data.email, data.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, db: DBSession):
    repo = UserRepository(db)
    service = AuthService(repo)
    return await service.refresh_token(data.refresh_token)
```

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, Query
from app.dependencies import DBSession, CurrentUser, require_role
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserUpdate, UserList

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user


@router.get("/", response_model=UserList)
async def list_users(
    db: DBSession,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    repo = UserRepository(db)
    service = UserService(repo)
    items, total = await service.list_users(skip=(page - 1) * limit, limit=limit)
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": -(-total // limit),  # ceil division
    }


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: DBSession):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    data: UserUpdate,
    db: DBSession,
    current_user: CurrentUser,
):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.update_user(user_id, data.model_dump(exclude_unset=True))


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    db: DBSession,
    admin_user: CurrentUser = Depends(require_role("admin")),
):
    repo = UserRepository(db)
    service = UserService(repo)
    await service.delete_user(user_id)
```

---

## 12. Error Handling

```python
# app/exceptions.py
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI


class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500, detail: dict = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail


class NotFoundError(AppException):
    def __init__(self, entity: str = "Resource"):
        super().__init__(f"{entity} not found", status_code=404)


class ConflictError(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class ValidationError(AppException):
    def __init__(self, message: str = "Validation failed", detail: dict = None):
        super().__init__(message, status_code=422, detail=detail)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.status_code,
                    "message": exc.message,
                    "detail": exc.detail,
                },
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": 500,
                    "message": "Internal server error",
                },
            },
        )
```

---

## 13. Custom Middleware

```python
# app/middleware.py
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        logger.info(
            "%s %s %s %.2fms",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-MS"] = str(round(process_time, 2))

        return response
```

---

## 14. Background Tasks

```python
# Using FastAPI's built-in BackgroundTasks (lightweight)
from fastapi import BackgroundTasks


def send_welcome_email(email: str):
    # Simulate email sending
    import time
    time.sleep(2)
    print(f"Welcome email sent to {email}")


@router.post("/register", status_code=201)
async def register(
    data: UserCreate,
    db: DBSession,
    background_tasks: BackgroundTasks,
):
    repo = UserRepository(db)
    service = UserService(repo)
    user = await service.create_user(data)

    background_tasks.add_task(send_welcome_email, user.email)
    return user


# Using Celery (heavy tasks)
# app/workers/celery_app.py
from celery import Celery
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.task_routes = {"app.workers.tasks.*": {"queue": "default"}}
```

```python
# app/workers/tasks/email_tasks.py
from app.workers.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email_task(self, email: str, name: str):
    try:
        # Send email logic
        print(f"Sending welcome email to {name} <{email}>")
        return True
    except Exception as exc:
        raise self.retry(exc=exc)
```

---

## 15. Pagination Utility

```python
# app/utils/pagination.py
from math import ceil
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_prev: bool


def paginate(items: list, total: int, page: int, limit: int) -> dict:
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": max(1, ceil(total / limit)),
        "has_next": page * limit < total,
        "has_prev": page > 1,
    }
```

---

## 16. File Upload

```python
from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import uuid
from pathlib import Path

router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "application/pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"File type {file.content_type} not allowed")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    filepath = UPLOAD_DIR / filename

    with open(filepath, "wb") as f:
        f.write(contents)

    return {
        "filename": filename,
        "size": len(contents),
        "content_type": file.content_type,
        "url": f"/uploads/{filename}",
    }


@router.post("/uploads/multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        contents = await file.read()
        ext = Path(file.filename).suffix
        filename = f"{uuid.uuid4()}{ext}"
        with open(UPLOAD_DIR / filename, "wb") as f:
            f.write(contents)
        results.append({"filename": filename, "size": len(contents)})
    return {"files": results}
```

---

## 17. Rate Limiting

```python
# app/middleware/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address)

# In app factory:
# app.state.limiter = limiter
# app.add_middleware(SlowAPIMiddleware)


@router.get("/users")
@limiter.limit("100/minute")
async def list_users(request: Request, db: DBSession):
    # ...
    pass


@router.post("/auth/login")
@limiter.limit("10/minute")  # Stricter for auth endpoints
async def login(request: Request, data: LoginRequest, db: DBSession):
    # ...
    pass
```

---

## 18. Logging (Structured JSON)

```python
# app/logging_config.py
import json
import logging
import sys
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_logging(level: str = "INFO"):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(level)
```

---

## 19. Testing

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import create_app
from app.database import Base, get_db
from app.config import get_settings

# Use SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine):
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    app = create_app()

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
```

```python
# tests/test_users.py
import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data  # Password should never be returned


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "password123", "name": "Dup"},
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "password123", "name": "Dup"},
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login@test.com", "password": "password123", "name": "Login"},
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@test.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_me_unauthorized(client):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authorized(client):
    # Register + login
    await client.post(
        "/api/v1/auth/register",
        json={"email": "me@test.com", "password": "password123", "name": "Me"},
    )
    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": "me@test.com", "password": "password123"},
    )
    token = login_res.json()["access_token"]

    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@test.com"
```

---

## 20. WebSocket

```python
from fastapi import WebSocket, WebSocketDisconnect
from app.dependencies import get_current_user


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str = "general"):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str = "general"):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)

    async def broadcast(self, message: str, room: str = "general"):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"User says: {data}", room)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        await manager.broadcast(f"User left {room}", room)
```

---

## 21. Redis Caching

```python
# app/integrations/cache.py
import json
from functools import wraps
from typing import Optional, Any
import redis.asyncio as redis
from app.config import get_settings

settings = get_settings()

class Cache:
    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def init(self):
        if settings.REDIS_URL:
            self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get(self, key: str) -> Any:
        if not self.client:
            return None
        value = await self.client.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: Any, ttl: int = 300):
        if not self.client:
            return
        await self.client.setex(key, ttl, json.dumps(value))

    async def delete(self, key: str):
        if self.client:
            await self.client.delete(key)


cache = Cache()


def cached(ttl: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build a cache key from function name and args
            key = f"{func.__name__}:{hash(frozenset(kwargs.items()))}"
            cached_result = await cache.get(key)
            if cached_result is not None:
                return cached_result

            result = await func(*args, **kwargs)
            await cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator


# Usage:
# @router.get("/products")
# @cached(ttl=60)
# async def list_products(db: DBSession):
#     ...
```

---

## 22. Dependency Injection with Service Layer

```python
# app/dependencies.py (extended)
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService


def get_user_repository(db: DBSession) -> UserRepository:
    return UserRepository(db)


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


def get_auth_service(repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repo)


UserServiceDI = Annotated[UserService, Depends(get_user_service)]
AuthServiceDI = Annotated[AuthService, Depends(get_auth_service)]


# Usage:
# @router.get("/users/me")
# async def get_me(
#     service: UserServiceDI,
#     current_user: CurrentUser,
# ):
#     return await service.get_user(str(current_user.id))
```

---

## 23. Alembic Async Migration Config

```python
# alembic/env.py
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.database import Base
from app.models import User  # noqa: import all models
from app.config import get_settings

config = context.config
settings = get_settings()
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

_These patterns target FastAPI with Pydantic v2, async SQLAlchemy 2.0, and JWT auth. The key architecture: **routers** are thin (HTTP only), **services** contain business logic, **repositories** handle data access, and **dependencies** wire everything together with `Depends()`._
