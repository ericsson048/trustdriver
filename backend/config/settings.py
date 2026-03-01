from pathlib import Path
import os
from urllib.parse import parse_qs, urlparse


BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BACKEND_DIR.parent
FRONTEND_DIST_DIR = next(
    (
        candidate
        for candidate in (BACKEND_DIR / "dist", REPO_DIR / "dist")
        if candidate.exists()
    ),
    REPO_DIR / "dist",
)


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    return [
        item.strip()
        for item in os.getenv(name, default).split(",")
        if item.strip()
    ]


load_env_file(BACKEND_DIR / ".env")


def database_config_from_url(url: str) -> dict:
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()

    if scheme not in {"postgres", "postgresql"}:
        raise ValueError("Only PostgreSQL DATABASE_URL values are supported.")

    query = parse_qs(parsed.query)
    options: dict[str, str] = {}

    sslmode = query.get("sslmode", [None])[0]
    channel_binding = query.get("channel_binding", [None])[0]

    if sslmode:
        options["sslmode"] = sslmode
    if channel_binding:
        options["channel_binding"] = channel_binding

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": parsed.path.lstrip("/"),
        "USER": parsed.username or "",
        "PASSWORD": parsed.password or "",
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or 5432),
        "OPTIONS": options,
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "60")),
        "CONN_HEALTH_CHECKS": True,
    }


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-change-this")
DEBUG = env_bool("DJANGO_DEBUG", False)

default_allowed_hosts = {
    "127.0.0.1",
    "localhost",
    "trustdriver.onrender.com",
}

for candidate in (
    os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip(),
    urlparse(os.getenv("RENDER_EXTERNAL_URL", "").strip()).hostname or "",
):
    if candidate:
        default_allowed_hosts.add(candidate)

ALLOWED_HOSTS = sorted(
    default_allowed_hosts.union(env_list("DJANGO_ALLOWED_HOSTS"))
)

default_frontend_origins = {
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://trustdriver.vercel.app",
}

FRONTEND_ORIGINS = sorted(
    default_frontend_origins.union(env_list("DJANGO_FRONTEND_ORIGINS"))
)
CSRF_TRUSTED_ORIGINS = FRONTEND_ORIGINS
FRONTEND_APP_URL = os.getenv(
    "FRONTEND_APP_URL",
    next(
        (origin for origin in FRONTEND_ORIGINS if origin.startswith("https://")),
        FRONTEND_ORIGINS[0] if FRONTEND_ORIGINS else "http://localhost:5173",
    ),
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "apps.accounts",
    "apps.api_docs",
    "apps.drive",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "config.middleware.SimpleCorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [FRONTEND_DIST_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL:
    DATABASES = {
        "default": database_config_from_url(DATABASE_URL),
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BACKEND_DIR / "backend.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BACKEND_DIR / "staticfiles"
STATICFILES_DIRS = [FRONTEND_DIST_DIR] if FRONTEND_DIST_DIR.exists() else []

MEDIA_URL = "/media/"
MEDIA_ROOT = BACKEND_DIR / "media"

AUTH_USER_MODEL = "accounts.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = "Lax" if DEBUG else "None"
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax" if DEBUG else "None"

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "TrustDriver <noreply@trustdriver.app>")
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "").strip()
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", DEFAULT_FROM_EMAIL)
EMAIL_VERIFICATION_TOKEN_TTL_HOURS = int(os.getenv("EMAIL_VERIFICATION_TOKEN_TTL_HOURS", "24"))

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "TrustDriver API",
    "DESCRIPTION": "Documentation des endpoints d'authentification, fichiers et partage.",
    "VERSION": "1.0.0",
}
