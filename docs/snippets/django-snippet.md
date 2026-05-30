# Useful Django Codeblock Patterns

> Practical, copy-paste-ready Django & Django REST Framework patterns for building production applications.

---

## 1. Project Structure

```
project/
  config/
    __init__.py
    settings/
      __init__.py
      base.py            # Shared settings
      development.py     # Dev-specific settings
      production.py      # Production settings
    urls.py              # Root URL config
    wsgi.py
    asgi.py
  apps/
    users/               # Auth, profile, permissions
      __init__.py
      models.py
      views.py
      serializers.py
      urls.py
      services.py        # Business logic
      selectors.py       # Query logic
      tests.py
      admin.py
    orders/
      __init__.py
      models.py
      views.py
      serializers.py
      urls.py
      services.py
      tests.py
  services/              # Cross-app business logic orchestration
  integrations/          # Stripe, Twilio, OpenAI, AWS wrappers
  tasks/                 # Celery background jobs
  static/
  templates/
  manage.py
  requirements/
    base.txt
    development.txt
    production.txt
  Dockerfile
  docker-compose.yml
```

---

## 2. Split Settings by Environment

```python
# config/settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "corsheaders",
    "django_filters",
    # Local apps
    "apps.users",
    "apps.orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/min",
        "user": "1000/min",
    },
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}
```

```python
# config/settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "myapp_dev"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1"]
```

```python
# config/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {"sslmode": "require"},
    }
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```

---

## 3. Custom User Model

```python
# apps/users/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20,
        choices=[("user", "User"), ("admin", "Admin"), ("manager", "Manager")],
        default="user",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return self.email
```

```python
# config/settings/base.py (add at the top)
AUTH_USER_MODEL = "users.User"
```

```python
# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "is_active", "is_verified")
    list_filter = ("role", "is_active", "is_verified")
    search_fields = ("email", "username")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "phone", "company")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "is_verified", "groups")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
```

---

## 4. Model Patterns

### Base Model with UUID and Timestamps

```python
# apps/core/models.py
import uuid
from django.db import models


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(TimeStampedMixin, UUIDModel):
    class Meta:
        abstract = True
```

### Domain Model Example

```python
# apps/orders/models.py
from django.db import models
from apps.core.models import BaseModel


class Order(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    customer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = "orders"
        indexes = [
            models.Index(fields=["customer", "status"]),
            models.Index(fields=["-created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} — {self.customer.email}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_items"

    @property
    def subtotal(self) -> Decimal:
        return self.quantity * self.unit_price
```

---

## 5. DRF Serializers

### Basic Serializer

```python
# apps/orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "quantity", "unit_price", "subtotal"]
        read_only_fields = ["id"]


class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    customer_email = serializers.EmailField(source="customer.email", read_only=True)
    item_count = serializers.IntegerField(source="items.count", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer_email", "status", "total", "item_count", "created_at"]
        read_only_fields = ["id", "created_at"]


class OrderDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail views."""
    customer = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "status", "total", "shipping_address", "notes", "items", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_customer(self, obj):
        return {"id": str(obj.customer.id), "email": obj.customer.email, "name": obj.customer.username}


class OrderCreateSerializer(serializers.Serializer):
    """Separate write serializer — validates input, no model binding."""
    items = OrderItemSerializer(many=True)
    shipping_address = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one item is required")
        return items
```

### Split Read/Write Serializers

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "is_active"]
        read_only_fields = ["id", "role"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "phone", "company"]
```

### Serializer with Custom Validation

```python
class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)
    reason = serializers.CharField(required=False, allow_blank=True)

    def validate_status(self, value):
        if value == Order.Status.CANCELLED and not self.initial_data.get("reason"):
            raise serializers.ValidationError("Reason is required for cancellation")
        return value
```

---

## 6. ViewSets and Routers

### Basic ModelViewSet

```python
# apps/orders/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
)
from .services import OrderService


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status"]
    search_fields = ["notes", "shipping_address"]
    ordering_fields = ["created_at", "total", "status"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderDetailSerializer
        if self.action == "create":
            return OrderCreateSerializer
        return OrderDetailSerializer

    def get_queryset(self):
        # Tenant isolation — always scope to current user
        return (
            Order.objects
            .filter(customer=self.request.user)
            .select_related("customer")
            .prefetch_related("items")
        )

    def perform_create(self, serializer):
        service = OrderService()
        order = service.create_order(
            customer=self.request.user,
            data=serializer.validated_data,
        )
        return order

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = OrderService()
        result = service.cancel_order(order, reason=serializer.validated_data.get("reason"))
        return Response(OrderDetailSerializer(result).data)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Custom endpoint: /orders/summary/"""
        queryset = self.get_queryset()
        return Response({
            "total": queryset.count(),
            "pending": queryset.filter(status="pending").count(),
            "total_revenue": sum(o.total for o in queryset.filter(status="delivered")),
        })
```

### ReadOnly ModelViewSet

```python
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related("category")
    serializer_class = ProductSerializer
    permission_classes = []  # Public read-only
    filterset_fields = ["category", "is_featured"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "created_at"]
```

### Base ViewSet with Common Behavior

```python
# apps/core/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class BaseModelViewSet(viewsets.ModelViewSet):
    """All viewsets inherit from this to enforce tenant isolation."""
    permission_classes = [IsAuthenticated]
    owner_field = "customer"  # Override in subclasses

    def get_queryset(self):
        return self.model.objects.filter(**{self.owner_field: self.request.user})
```

---

## 7. Routers and URLs

```python
# apps/orders/urls.py
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = router.urls
```

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.orders.urls")),
    path("api/v1/", include("apps.users.urls")),
    path("api/auth/", include("rest_framework_simplejwt.urls")),
]
```

---

## 8. Service Layer (Business Logic)

```python
# apps/orders/services.py
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.orders.models import Order, OrderItem
from apps.orders.selectors import OrderSelector
from apps.integrations.email import send_order_confirmation


class OrderService:
    def create_order(self, customer, data) -> Order:
        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                shipping_address=data["shipping_address"],
                notes=data.get("notes", ""),
                total=self._calculate_total(data["items"]),
            )

            for item_data in data["items"]:
                OrderItem.objects.create(
                    order=order,
                    product_name=item_data["product_name"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                )

        # Side effect after transaction commits
        transaction.on_commit(lambda: send_order_confirmation.delay(str(order.id)))

        return order

    def cancel_order(self, order, reason: str = "") -> Order:
        if order.status in (Order.Status.SHIPPED, Order.Status.DELIVERED):
            raise ValidationError("Cannot cancel shipped or delivered orders")

        with transaction.atomic():
            order.status = Order.Status.CANCELLED
            order.notes = f"{order.notes}\n[CANCELLED] {reason}".strip()
            order.save()

        transaction.on_commit(lambda: self._handle_cancellation_side_effects(order))
        return order

    def _calculate_total(self, items: list) -> Decimal:
        return sum(Decimal(item["quantity"]) * Decimal(item["unit_price"]) for item in items)

    def _handle_cancellation_side_effects(self, order):
        # Refund, notify, etc.
        pass
```

### Service with Dependency Injection

```python
# apps/users/services.py
from django.contrib.auth import get_user_model
from django.db import transaction
from integrations.email import EmailService

User = get_user_model()


class UserService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def register_user(self, email: str, password: str, username: str) -> User:
        with transaction.atomic():
            user = User.objects.create_user(
                email=email, password=password, username=username
            )
            # Side effects
            transaction.on_commit(
                lambda: self.email_service.send_welcome_email(user.email, user.username)
            )
        return user

    def verify_user(self, user: User) -> User:
        user.is_verified = True
        user.save()
        return user
```

---

## 9. Selectors (Query Logic)

```python
# apps/orders/selectors.py
from django.db.models import Prefetch, Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem


class OrderSelector:
    def get_orders_for_user(self, user, status=None):
        queryset = Order.objects.filter(customer=user).select_related("customer")
        if status:
            queryset = queryset.filter(status=status)
        return queryset.prefetch_related(
            Prefetch("items", queryset=OrderItem.objects.select_related("order"))
        )

    def get_pending_orders(self, since_hours: int = 24):
        cutoff = timezone.now() - timedelta(hours=since_hours)
        return (
            Order.objects
            .filter(status=Order.Status.PENDING, created_at__gte=cutoff)
            .select_related("customer")
        )

    def get_order_stats(self, user):
        return Order.objects.filter(customer=user).aggregate(
            total_orders=Count("id"),
            total_spent=Sum("total"),
            pending_count=Count("id", filter=Q(status=Order.Status.PENDING)),
            delivered_count=Count("id", filter=Q(status=Order.Status.DELIVERED)),
        )
```

---

## 10. Permissions

### Custom Permission Classes

```python
# apps/core/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Object-level permission. Only owners can edit."""
    owner_field = "customer"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, self.owner_field) == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsRole(BasePermission):
    """Permission factory — checks user.role."""
    def __init__(self, *allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.allowed_roles


# Usage:
# permission_classes = [IsAuthenticated, IsRole("admin", "manager")]


class IsSupportAgent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff and request.user.groups.filter(name="support").exists()
```

### Permission per Action

```python
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        if self.action == "destroy":
            return [IsAuthenticated(), IsRole("admin")]
        if self.action == "cancel":
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsAuthenticated()]
```

---

## 11. Pagination

### Custom Pagination Classes

```python
# apps/core/pagination.py
from rest_framework.pagination import PageNumberPagination, CursorPagination


class StandardResultsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class LargeResultsPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class CursorOrderPagination(CursorPagination):
    page_size = 20
    ordering = "-created_at"
```

```python
# Usage in ViewSet:
# pagination_class = StandardResultsPagination
# Or set globally:
# REST_FRAMEWORK = { "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardResultsPagination" }
```

---

## 12. Filtering

### Basic Filtering

```python
# apps/orders/views.py
class OrderViewSet(viewsets.ModelViewSet):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "customer__email"]
    search_fields = ["notes", "shipping_address", "customer__email"]
    ordering_fields = ["created_at", "total", "status"]
    ordering = ["-created_at"]
```

### Advanced FilterSet

```python
# apps/orders/filters.py
import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Order.Status.choices)
    min_total = django_filters.NumberFilter(field_name="total", lookup_expr="gte")
    max_total = django_filters.NumberFilter(field_name="total", lookup_expr="lte")
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    customer_email = django_filters.CharFilter(field_name="customer__email", lookup_expr="icontains")
    has_notes = django_filters.BooleanFilter(field_name="notes", lookup_expr="gt", method="filter_has_notes")

    def filter_has_notes(self, queryset, name, value):
        if value:
            return queryset.exclude(notes="")
        return queryset.filter(notes="")

    class Meta:
        model = Order
        fields = ["status", "min_total", "max_total", "created_after", "created_before"]
```

```python
# Usage in ViewSet:
# filterset_class = OrderFilter
```

---

## 13. Signals

### Safe Signal Pattern (with transaction.on_commit)

```python
# apps/orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Order


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    """Enqueue side-effects only after the DB transaction commits."""
    if created:
        transaction.on_commit(
            lambda: send_order_confirmation_email.delay(str(instance.id))
        )

    if instance.status == Order.Status.CANCELLED:
        transaction.on_commit(
            lambda: process_refund.delay(str(instance.id))
        )
```

```python
# apps/orders/apps.py
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.orders"

    def ready(self):
        import apps.orders.signals  # noqa
```

---

## 14. Custom Management Commands

```python
# apps/orders/management/commands/cleanup_expired_orders.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Order


class Command(BaseCommand):
    help = "Cancel pending orders older than N days"

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=7, help="Age in days")

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=options["days"])
        expired = Order.objects.filter(
            status=Order.Status.PENDING,
            created_at__lt=cutoff,
        )
        count = expired.count()
        expired.update(status=Order.Status.CANCELLED)
        self.stdout.write(self.style.SUCCESS(f"Cancelled {count} expired orders"))
```

```python
# Running:
# python manage.py cleanup_expired_orders --days 30
```

---

## 15. Custom Exception Handler

```python
# apps/core/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = []
        if isinstance(response.data, dict):
            for field, messages in response.data.items():
                if isinstance(messages, list):
                    for msg in messages:
                        errors.append({"field": field, "message": str(msg)})
                else:
                    errors.append({"field": field, "message": str(messages)})
        else:
            errors = [{"message": str(response.data)}]

        response.data = {
            "success": False,
            "status_code": response.status_code,
            "errors": errors,
        }
    else:
        # Unhandled exceptions
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        response = Response(
            {
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "errors": [{"message": "Internal server error"}],
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
```

---

## 16. Throttling

```python
# settings/base.py
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        "login": "10/minute",
        "uploads": "20/hour",
    },
}
```

```python
# Per-view throttle scope
class LoginView(TokenObtainPairView):
    throttle_scope = "login"


class FileUploadView(APIView):
    throttle_scope = "uploads"
```

---

## 17. JWT Authentication (SimpleJWT)

```python
# settings/base.py
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
```

```python
# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

---

## 18. Celery Background Tasks

```python
# tasks/celery_app.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

```python
# tasks/email_tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation_email(self, order_id):
    from apps.orders.models import Order
    try:
        order = Order.objects.get(id=order_id)
        send_mail(
            subject=f"Order {order.id} confirmed",
            message=f"Your order of ${order.total} has been confirmed.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer.email],
            fail_silently=False,
        )
    except Order.DoesNotExist:
        return
    except Exception as exc:
        raise self.retry(exc=exc)
```

```python
# settings/base.py
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
```

---

## 19. Testing

```python
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.development
python_files = tests.py test_*.py *_tests.py
```

```python
# apps/orders/tests.py
import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.orders.models import Order
from apps.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="test@example.com",
        password="password123",
        username="testuser",
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def order(db, user):
    return Order.objects.create(
        customer=user,
        total=Decimal("99.99"),
        shipping_address="123 Main St",
    )


@pytest.mark.django_db
class TestOrderAPI:
    def test_list_orders(self, auth_client, order):
        url = reverse("order-list")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_create_order(self, auth_client):
        url = reverse("order-list")
        data = {
            "items": [
                {"product_name": "Widget", "quantity": 2, "unit_price": "24.99"},
            ],
            "shipping_address": "456 Oak St",
        }
        response = auth_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1

    def test_retrieve_order(self, auth_client, order):
        url = reverse("order-detail", kwargs={"pk": order.pk})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert str(response.data["id"]) == str(order.pk)

    def test_cancel_order(self, auth_client, order):
        url = reverse("order-cancel", kwargs={"pk": order.pk})
        response = auth_client.post(url, {"reason": "Changed mind"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == Order.Status.CANCELLED

    def test_unauthorized_access(self, api_client):
        url = reverse("order-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_tenant_isolation(self, auth_client, user):
        # Create another user's order
        other_user = User.objects.create_user(
            email="other@example.com", password="password123", username="other"
        )
        Order.objects.create(customer=other_user, total=Decimal("10.00"), shipping_address="Other")

        url = reverse("order-list")
        response = auth_client.get(url)
        # Should only see the current user's orders
        assert response.data["count"] == 0


@pytest.mark.django_db
class TestOrderService:
    def test_create_order_with_items(self, user):
        from apps.orders.services import OrderService
        service = OrderService()

        data = {
            "items": [
                {"product_name": "Widget", "quantity": 2, "unit_price": "24.99"},
            ],
            "shipping_address": "456 Oak St",
        }
        order = service.create_order(customer=user, data=data)
        assert order.items.count() == 1
        assert order.total == Decimal("49.98")
```

---

## 20. Management Commands for Data

```python
# apps/core/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.orders.models import Order, OrderItem


class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        user, _ = User.objects.get_or_create(
            email="admin@example.com",
            defaults={"username": "admin"},
        )
        user.set_password("admin123")
        user.is_staff = True
        user.save()

        order = Order.objects.create(
            customer=user,
            total=Decimal("149.99"),
            shipping_address="789 Pine St",
        )
        OrderItem.objects.create(
            order=order,
            product_name="Premium Widget",
            quantity=1,
            unit_price=Decimal("149.99"),
        )

        self.stdout.write(self.style.SUCCESS("Data seeded successfully"))
```

---

## 21. Health Check Endpoint

```python
# apps/health/views.py
from django.db import connection
from django.http import JsonResponse
from django.views import View


class HealthCheckView(View):
    def get(self, request):
        health = {"status": "ok", "version": "1.0.0"}

        # Database check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            health["database"] = "ok"
        except Exception as e:
            health["database"] = "error"
            health["status"] = "degraded"

        return JsonResponse(health)
```

```python
# config/urls.py
from apps.health.views import HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health_check"),
    # ...
]
```

---

## 22. Django Ninja (Alternative to DRF)

```python
# api/schemas.py
from ninja import Schema
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class OrderItemSchema(Schema):
    product_name: str
    quantity: int
    unit_price: float


class OrderCreateSchema(Schema):
    items: List[OrderItemSchema]
    shipping_address: str
    notes: Optional[str] = ""


class OrderOutSchema(Schema):
    id: UUID
    status: str
    total: float
    created_at: datetime
    items: List[OrderItemSchema]
```

```python
# api/endpoints.py
from ninja import Router
from django.shortcuts import get_object_or_404
from apps.orders.models import Order
from apps.orders.services import OrderService
from .schemas import OrderCreateSchema, OrderOutSchema

router = Router()


@router.get("/orders", response=list[OrderOutSchema])
def list_orders(request):
    return Order.objects.filter(customer=request.user).select_related("customer")


@router.post("/orders", response=OrderOutSchema, url_attributes={"detail": "Create a new order"})
def create_order(request, data: OrderCreateSchema):
    service = OrderService()
    return service.create_order(customer=request.user, data=data.dict())


@router.get("/orders/{order_id}", response=OrderOutSchema)
def get_order(request, order_id: str):
    return get_object_or_404(Order, id=order_id, customer=request.user)
```

```python
# config/urls.py (Django Ninja)
from ninja import NinjaAPI
from api.endpoints import router as api_router

api = NinjaAPI(title="MyApp API", version="1.0.0")
api.add_router("/v1", api_router)

urlpatterns = [
    path("api/", api.urls),
]
```

---

*These patterns follow a layered architecture: **routers/views** handle HTTP, **services** contain business logic, **selectors** handle queries, and **models** handle persistence. Split settings by environment, use a custom user model from day one, and keep side effects behind `transaction.on_commit`.*
