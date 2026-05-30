# Useful Python Codeblock Patterns

> Practical, copy-paste-ready Python patterns for building production-grade applications.

---

## 1. Project Structure (src layout)

```
my-project/
  src/
    my_package/
      __init__.py
      __version__.py
      core/              # Pure business logic (no I/O)
        __init__.py
        models.py        # Dataclasses, Pydantic models
        engine.py        # Core computation logic
        validators.py    # Validation, constraints
      adapters/          # I/O (DB, API, files)
        __init__.py
        database.py
        api_client.py
        file_handler.py
      services/          # Orchestration (links core + adapters)
        __init__.py
        pipeline.py
      cli/               # CLI interface
        __init__.py
        main.py
  tests/
    __init__.py
    conftest.py
    unit/
    integration/
  pyproject.toml
  Dockerfile
  README.md
```

---

## 2. pyproject.toml

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "My awesome package"
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
    "click>=8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "mypy>=1.8",
    "ruff>=0.3",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
strict = true
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
```

---

## 3. Type Hints

### Basic Typing

```python
from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar, Generic, Optional, Union, Any


# Python 3.10+ built-in types
name: str = "Alice"
count: int = 42
price: float = 19.99
is_active: bool = True
tags: list[str] = ["python", "api"]
metadata: dict[str, Any] = {"version": 1}
coordinates: tuple[float, float] = (40.7128, -74.0060)
unique_ids: set[int] = {1, 2, 3}
maybe_value: Optional[int] = None  # Python 3.10+: int | None


# Functions
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"


# Union
def process_id(id: int | str) -> str:
    return str(id)


# TypeVar for generics
T = TypeVar("T")


def first(items: Sequence[T]) -> T | None:
    return items[0] if items else None
```

### TypedDict

```python
from typing import TypedDict


class UserDict(TypedDict):
    id: str
    name: str
    email: str
    age: int | None


def create_user(data: UserDict) -> UserDict:
    return {"id": "123", "name": data["name"], "email": data["email"], "age": data.get("age")}
```

### Protocol (Structural Subtyping)

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class DataFetcher(Protocol):
    def fetch(self, url: str) -> dict[str, Any]: ...

    async def fetch_async(self, url: str) -> dict[str, Any]: ...


class HTTPClient:
    def fetch(self, url: str) -> dict[str, Any]:
        # Implementation
        return {"data": "response"}

    async def fetch_async(self, url: str) -> dict[str, Any]:
        # Async implementation
        return {"data": "response"}


# HTTPClient satisfies DataFetcher protocol implicitly
def get_data(fetcher: DataFetcher, url: str) -> dict[str, Any]:
    return fetcher.fetch(url)


client = HTTPClient()
result = get_data(client, "https://api.example.com")
```

### Literal and Never

```python
from typing import Literal, Never, assert_never
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELLED = "cancelled"


def handle_status(status: Literal["pending", "active", "cancelled"]) -> str:
    match status:
        case "pending":
            return "Waiting"
        case "active":
            return "Running"
        case "cancelled":
            return "Stopped"
        # Type checker ensures all cases are handled


def assert_exhaustive(value: Never) -> None:
    """Helper to ensure all enum cases are handled."""
    assert_never(value)
```

---

## 4. Dataclasses

### Basic Dataclass

```python
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class User:
    name: str
    email: str
    age: Optional[int] = None
    tags: list[str] = field(default_factory=list)


# Usage
user = User(name="Alice", email="alice@example.com", tags=["admin"])
print(user)  # User(name='Alice', email='alice@example.com', age=None, tags=['admin'])
```

### Frozen (Immutable) Dataclass

```python
@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float

    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Invalid latitude: {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Invalid longitude: {self.longitude}")


point = Coordinates(40.7128, -74.0060)
# point.latitude = 0  # Error: cannot assign to frozen field
```

### Dataclass with Slots (Python 3.10+)

```python
@dataclass(slots=True)
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
```

### Dataclass Inheritance

```python
@dataclass
class BaseModel:
    id: str
    created_at: str


@dataclass
class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True
```

---

## 5. Pydantic v2 Models

### Basic Model

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID, uuid4
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    tags: list[str] = []

    @field_validator("name")
    @classmethod
    def name_must_be_capitalized(cls, v: str) -> str:
        if not v[0].isupper():
            raise ValueError("Name must start with uppercase")
        return v


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}  # ORM mode

    id: UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime


# Usage
user = UserCreate(name="Alice", email="alice@example.com", age=30)
print(user.model_dump_json())
# {"name": "Alice", "email": "alice@example.com", "age": 30, "tags": []}
```

### Nested Models

```python
from pydantic import BaseModel
from typing import List


class OrderItem(BaseModel):
    product_name: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: str
    items: List[OrderItem] = Field(min_length=1)
    shipping_address: str
    notes: str | None = None
```

### Settings with Pydantic

```python
from pydantic import Field, field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "MyApp"
    DEBUG: bool = False
    SECRET_KEY: str = Field(..., min_length=32)

    DATABASE_URL: PostgresDsn
    REDIS_URL: Optional[str] = None

    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    LOG_LEVEL: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## 6. Decorators

### Basic Decorator with functools.wraps

```python
import time
from functools import wraps
from typing import Callable, Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure and log execution time."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed * 1000:.2f}ms")
        return result

    return wrapper


@timer
def compute_something(n: int) -> int:
    return sum(range(n))
```

### Decorator with Arguments (Three-Layer Pattern)

```python
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry a function on failure with exponential backoff."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    if attempt < max_attempts:
                        sleep_time = delay * (2 ** (attempt - 1))
                        print(f"Attempt {attempt} failed. Retrying in {sleep_time:.1f}s...")
                        time.sleep(sleep_time)
            raise last_exception  # type: ignore

        return wrapper

    return decorator


@retry(max_attempts=3, delay=0.5)
def fetch_data(url: str) -> dict:
    # Simulate flaky network call
    ...
```

### Class-Based Decorator

```python
class CountCalls:
    """Decorator class that counts function calls."""

    def __init__(self, func: Callable) -> None:
        self.func = func
        self.count = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.count += 1
        print(f"{self.func.__name__} called {self.count} times")
        return self.func(*args, **kwargs)


@CountCalls
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

### Async Decorator

```python
import asyncio
from functools import wraps


def async_retry(max_attempts: int = 3, delay: float = 1.0):
    """Async retry decorator with exponential backoff."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    if attempt < max_attempts:
                        await asyncio.sleep(delay * (2 ** (attempt - 1)))
            raise last_exception

        return wrapper

    return decorator
```

### Deprecation Decorator

```python
import warnings


def deprecated(message: str = ""):
    """Mark a function as deprecated."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
```

---

## 7. Context Managers

### Class-Based Context Manager

```python
class ManagedFile:
    """Context manager for file operations."""

    def __init__(self, filename: str, mode: str = "r") -> None:
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False  # Don't suppress exceptions


# Usage
with ManagedFile("data.txt", "w") as f:
    f.write("Hello, world!")
```

### contextmanager Decorator

```python
from contextlib import contextmanager
from typing import Generator


@contextmanager
def database_transaction(db) -> Generator[None, None, None]:
    """Context manager for database transactions."""
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise
```

### Async Context Manager

```python
from contextlib import asynccontextmanager


@asynccontextmanager
async def http_session():
    """Manage aiohttp session lifecycle."""
    import aiohttp

    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()


async def fetch_data(url: str) -> dict:
    async with http_session() as session:
        async with session.get(url) as response:
            return await response.json()
```

### Context Manager with Exception Handling

```python
@contextmanager
def temporary_change(obj, attr, value):
    """Temporarily change an object attribute, restoring it afterward."""
    original = getattr(obj, attr, None)
    setattr(obj, attr, value)
    try:
        yield
    finally:
        setattr(obj, attr, original)
```

---

## 8. Async/Await Patterns

### Basic Async Function

```python
import asyncio
from typing import List


async def fetch_user(user_id: str) -> dict:
    """Async function for I/O-bound operations."""
    await asyncio.sleep(0.1)  # Simulate network call
    return {"id": user_id, "name": "Alice"}


async def fetch_all_users(user_ids: List[str]) -> List[dict]:
    """Concurrent execution with asyncio.gather."""
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)
```

### TaskGroup (Python 3.11+)

```python
async def fetch_all_with_tasks(user_ids: list[str]) -> list[dict]:
    """TaskGroup provides better error handling than asyncio.gather."""
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_user(uid)) for uid in user_ids]

    # If any task raised, it propagates here and other tasks are cancelled
    return [task.result() for task in tasks]
```

### Async with Semaphore

```python
async def fetch_with_concurrency_limit(urls: list[str], max_concurrent: int = 5) -> list[dict]:
    """Limit concurrent requests with a semaphore."""
    sem = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> dict:
        async with sem:
            # Simulate HTTP request
            await asyncio.sleep(0.5)
            return {"url": url, "status": 200}

    tasks = [fetch_one(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### Timeout Handling

```python
async def fetch_with_timeout(url: str, timeout: float = 5.0) -> dict:
    """Fetch with a timeout."""
    try:
        async with asyncio.timeout(timeout):  # Python 3.11+
            await asyncio.sleep(10)
            return {"data": "response"}
    except TimeoutError:
        raise TimeoutError(f"Request to {url} timed out after {timeout}s")
```

---

## 9. Generators and Iterators

### Generator for Lazy Evaluation

```python
from typing import Generator


def read_large_file(filepath: str) -> Generator[str, None, None]:
    """Read a file line by line without loading it into memory."""
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def fibonacci() -> Generator[int, None, None]:
    """Infinite fibonacci sequence generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

### Generator with Send

```python
def accumulator() -> Generator[float, float, None]:
    """Accumulator generator that receives values via send()."""
    total = 0.0
    while True:
        value = yield total
        total += value


acc = accumulator()
next(acc)  # Initialize
print(acc.send(10))  # 10.0
print(acc.send(20))  # 30.0
print(acc.send(30))  # 60.0
```

### Async Generator

```python
from typing import AsyncGenerator


async def paginate_results(page_size: int = 100) -> AsyncGenerator[list[dict], None]:
    """Async generator for paginated API results."""
    page = 1
    while True:
        results = await fetch_page(page, page_size)
        if not results:
            return
        yield results
        page += 1


async def process_all():
    async for batch in paginate_results():
        process_batch(batch)
```

---

## 10. Dependency Injection

### Constructor Injection

```python
from typing import Protocol


class EmailService(Protocol):
    def send(self, to: str, subject: str, body: str) -> None: ...


class SmtpEmailService:
    def send(self, to: str, subject: str, body: str) -> None:
        print(f"Sending email to {to}: {subject}")


class UserService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def register_user(self, email: str, name: str) -> None:
        # Business logic
        self.email_service.send(email, "Welcome!", f"Hi {name}!")


# Production
service = UserService(SmtpEmailService())

# Test
from unittest.mock import Mock
mock_email = Mock()
test_service = UserService(mock_email)
```

### FastAPI-Style DI

```python
# Works with any async framework using similar patterns
class DatabaseSession:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    async def query(self, sql: str) -> list[dict]:
        return []


class ServiceProvider:
    def __init__(self):
        self._instances: dict = {}

    def get(self, cls, **kwargs):
        if cls not in self._instances:
            self._instances[cls] = cls(**kwargs)
        return self._instances[cls]


provider = ServiceProvider()
db = provider.get(DatabaseSession, connection_string="postgresql://...")
```

---

## 11. Logging

### Structured JSON Logging

```python
import json
import logging
import sys
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Log records as JSON lines."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)
        return json.dumps(log_entry)


def setup_logging(level: str = "INFO") -> logging.Logger:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(level)
    return root


logger = setup_logging("INFO")
logger.info("Server started", extra={"extra_fields": {"port": 8080, "env": "production"}})
```

### Structured Logging with Extra Fields

```python
import logging

logger = logging.getLogger(__name__)


def log_request(method: str, path: str, status: int, duration: float) -> None:
    logger.info(
        "HTTP request",
        extra={
            "extra_fields": {
                "method": method,
                "path": path,
                "status": status,
                "duration_ms": round(duration * 1000, 2),
            }
        },
    )
```

---

## 12. Error Handling

### Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500, detail: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, entity: str = "Resource"):
        super().__init__(f"{entity} not found", status_code=404)


class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class ValidationError(AppError):
    def __init__(self, message: str = "Validation failed", detail: dict | None = None):
        super().__init__(message, status_code=422, detail=detail)
```

### Result Type (Railway Oriented)

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class Result(Generic[T, E]):
    """Simple Result type for railway-oriented programming."""

    value: Optional[T] = None
    error: Optional[E] = None

    @classmethod
    def ok(cls, value: T) -> "Result[T, E]":
        return cls(value=value, error=None)

    @classmethod
    def fail(cls, error: E) -> "Result[T, E]":
        return cls(value=None, error=error)

    @property
    def is_ok(self) -> bool:
        return self.error is None

    @property
    def is_fail(self) -> bool:
        return self.error is not None

    def unwrap(self) -> T:
        if self.is_fail:
            raise ValueError(f"Called unwrap on error result: {self.error}")
        return self.value  # type: ignore

    def unwrap_or(self, default: T) -> T:
        return self.value if self.is_ok else default


# Usage
def divide(a: float, b: float) -> Result[float, str]:
    if b == 0:
        return Result.fail("Division by zero")
    return Result.ok(a / b)


result = divide(10, 2)
if result.is_ok:
    print(result.unwrap())  # 5.0
```

---

## 13. CLI with Click/Typer

### Click CLI

```python
import click


@click.group()
def cli():
    """CLI tool for managing the application."""
    pass


@cli.command()
@click.argument("name")
@click.option("--greeting", "-g", default="Hello", help="Greeting to use")
@click.option("--count", "-c", default=1, type=int, help="Number of times to greet")
def greet(name: str, greeting: str, count: int) -> None:
    """Greet a person."""
    for _ in range(count):
        click.echo(f"{greeting}, {name}!")


@cli.command()
@click.option("--port", "-p", default=8080, type=int, help="Port to run on")
@click.option("--debug", is_flag=True, help="Enable debug mode")
def serve(port: int, debug: bool) -> None:
    """Start the API server."""
    click.echo(f"Starting server on port {port} (debug={'on' if debug else 'off'})")


if __name__ == "__main__":
    cli()
# python app.py greet Alice --greeting "Hi" --count 3
# python app.py serve --port 3000 --debug
```

### Typer CLI

```python
import typer
from typing import Optional

app = typer.Typer()


@app.command()
def greet(
    name: str,
    greeting: str = typer.Option("Hello", "--greeting", "-g"),
    count: int = typer.Option(1, "--count", "-c"),
):
    """Greet a person."""
    for _ in range(count):
        print(f"{greeting}, {name}!")


@app.command()
def serve(
    port: int = typer.Option(8080, help="Port to run on"),
    debug: bool = typer.Option(False, help="Enable debug mode"),
):
    """Start the API server."""
    print(f"Starting server on port {port} (debug={'on' if debug else 'off'})")


if __name__ == "__main__":
    app()
```

---

## 14. Configuration

```python
import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration from environment variables."""

    def __init__(self) -> None:
        self.env: str = os.getenv("APP_ENV", "development")
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.secret_key: str = os.getenv("SECRET_KEY", "")

        # Database
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///app.db")
        self.db_pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))

        # Redis
        self.redis_url: str | None = os.getenv("REDIS_URL")

        # API
        self.api_prefix: str = "/api/v1"
        self.cors_origins: list[str] = os.getenv(
            "CORS_ORIGINS", "http://localhost:3000"
        ).split(",")

        # Paths
        self.base_dir: Path = Path(__file__).resolve().parent.parent
        self.log_dir: Path = self.base_dir / "logs"

    def validate(self) -> None:
        """Validate required configuration."""
        if not self.secret_key and self.env == "production":
            raise ValueError("SECRET_KEY is required in production")


@lru_cache
def get_config() -> Config:
    """Get cached config instance."""
    config = Config()
    config.validate()
    return config
```

---

## 15. Testing with pytest

### Fixtures

```python
import pytest
from unittest.mock import Mock, AsyncMock, patch


# Basic fixture
@pytest.fixture
def user_data() -> dict:
    return {"id": "123", "name": "Alice", "email": "alice@example.com"}


# Fixture with teardown
@pytest.fixture
def database():
    db = create_test_database()
    yield db
    db.drop()


# Async fixture
@pytest_asyncio.fixture
async def async_client():
    client = AsyncClient()
    yield client
    await client.aclose()


# Fixture with mock
@pytest.fixture
def mock_email_service():
    service = Mock()
    service.send.return_value = True
    return service
```

### Parametrized Tests

```python
@pytest.mark.parametrize(
    "input_value,expected",
    [
        (0.8, "high"),
        (0.3, "medium"),
        (-0.5, "low"),
        (0.0, "none"),
    ],
)
def test_signal_strength(input_value: float, expected: str) -> None:
    assert classify_strength(input_value) == expected
```

### Async Tests

```python
import pytest


@pytest.mark.asyncio
async def test_fetch_user() -> None:
    """Test async function."""
    user = await fetch_user("123")
    assert user["id"] == "123"
    assert user["name"] == "Alice"
```

### Mocking External Services

```python
from unittest.mock import patch


@patch("my_module.requests.get")
def test_fetch_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": "test"}

    result = fetch_data("https://api.example.com")
    assert result["data"] == "test"
    mock_get.assert_called_once_with("https://api.example.com")
```

### Property-Based Testing

```python
from hypothesis import given, strategies as st


@given(
    st.lists(st.integers(min_value=0, max_value=1000), min_length=1),
)
def test_sort_always_returns_sorted(numbers: list[int]) -> None:
    result = my_sort(numbers)
    assert all(result[i] <= result[i + 1] for i in range(len(result) - 1))
```

---

## 16. Performance Patterns

### LRU Cache

```python
from functools import lru_cache


@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    """Cache results of expensive function calls."""
    return sum(range(n)) ** 2
```

### TTL Cache

```python
import time
from functools import wraps
from threading import Lock


def ttl_cache(seconds: int = 60):
    """Decorator that caches results for a given TTL."""

    def decorator(func):
        cache = {}
        lock = Lock()

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str((args, frozenset(kwargs.items())))
            with lock:
                if key in cache:
                    result, timestamp = cache[key]
                    if time.time() - timestamp < seconds:
                        return result
                result = func(*args, **kwargs)
                cache[key] = (result, time.time())
                return result

        return wrapper

    return decorator


@ttl_cache(seconds=30)
def get_expensive_data() -> list[dict]:
    """Fetches data that changes infrequently."""
    ...
```

### Singleton Decorator

```python
from functools import wraps


def singleton(cls):
    """Decorator to make a class a singleton."""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class DatabasePool:
    def __init__(self):
        self.connections = []
```

### Timer Context Manager

```python
import time
from contextlib import contextmanager


@contextmanager
def timer(name: str = "operation"):
    """Context manager that logs execution time."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name} took {elapsed:.2f}ms")
```

---

## 17. Data Processing Patterns

### Chunked Processing

```python
from typing import Iterator, TypeVar

T = TypeVar("T")


def chunks(items: list[T], chunk_size: int) -> Iterator[list[T]]:
    """Yield successive chunks from a list."""
    for i in range(0, len(items), chunk_size):
        yield items[i : i + chunk_size]


# Usage
for batch in chunks(all_users, batch_size=100):
    process_batch(batch)
```

### Pipeline Pattern

```python
from dataclasses import dataclass
from typing import Callable


@dataclass
class Pipeline:
    """Simple pipeline for sequential data transformations."""

    steps: list[Callable]

    def run(self, data):
        result = data
        for step in self.steps:
            result = step(result)
        return result


# Usage
pipeline = Pipeline([
    lambda x: x.strip(),
    lambda x: x.lower(),
    lambda x: x.replace(" ", "_"),
])

cleaned = pipeline.run("  Hello World  ")  # "hello_world"
```

---

## 18. Enum Patterns

```python
from enum import Enum, auto, StrEnum


class Status(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELLED = "cancelled"


class Role(Enum):
    USER = auto()
    ADMIN = auto()
    MANAGER = auto()

    @property
    def permissions(self) -> list[str]:
        return {
            Role.USER: ["read"],
            Role.MANAGER: ["read", "write"],
            Role.ADMIN: ["read", "write", "delete", "manage"],
        }[self]


# Usage
role = Role.ADMIN
print(role.permissions)  # ['read', 'write', 'delete', 'manage']
print(Status.ACTIVE.value)  # 'active'
```

---

## 19. Serialization / Deserialization

```python
import json
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Event:
    id: str
    type: str
    payload: dict[str, Any]
    timestamp: str

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, data: str) -> "Event":
        return cls(**json.loads(data))
```

---

## 20. Clean Architecture Layer Separation

```python
# src/my_package/core/models.py — pure domain logic, no I/O
@dataclass(frozen=True)
class TradeSignal:
    symbol: str
    direction: float  # -1.0 to 1.0
    strength: float  # 0.0 to 1.0
    strategy: str
    timestamp: str

    def __post_init__(self):
        if not -1 <= self.direction <= 1:
            raise ValueError(f"direction must be in [-1, 1], got {self.direction}")
        if not 0 <= self.strength <= 1:
            raise ValueError(f"strength must be in [0, 1], got {self.strength}")

    @property
    def is_buy_signal(self) -> bool:
        return self.direction > 0.3


# src/my_package/adapters/database.py — I/O boundary
class UserRepository:
    def __init__(self, connection_string: str):
        self.conn_string = connection_string

    async def get_by_id(self, user_id: str) -> dict | None:
        # Database query
        ...


# src/my_package/services/pipeline.py — orchestration
class TradingPipeline:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    async def process_signal(self, signal: TradeSignal) -> None:
        user = await self.repo.get_by_id("123")
        if signal.is_buy_signal and user:
            # Execute trade
            ...
```

---

*Modern Python (3.11+) patterns: use `dataclass` for DTOs, `Protocol` for interfaces, `Pydantic` for validation, `Context managers` for resource safety, `asyncio` for concurrency, and `pyproject.toml` for configuration. Keep I/O separated from business logic.*
