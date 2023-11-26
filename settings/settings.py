import os

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# fortress/Fortress2/settings/base.py - 3 == 6p3/
ROOT_DIR = environ.Path(__file__) - 2

env = environ.Env()

sentry_sdk.init(
    dsn=env("SENTRY_DSN", default=None),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    environment=env("SENTRY_ENVIRONMENT_NAME", default="default"),
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "taggit",
    "modelcluster",
    "localflavor",
    "content",
    "documents",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "waunakeeairport.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "waunakeeairport.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WAGTAIL_SITE_NAME = "Waunakee Airport"
WAGTAILADMIN_BASE_URL = "https://www.waunakeeairport.com"


STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(ROOT_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, "media")

RUA_PDF_ROOT = os.path.join(ROOT_DIR, "media-rua")

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

SERVER_EMAIL = "Waunakee Airpark <fly@waunakeeairport.com>"

WAPA_SIGNUP_SEND_EMAIL_TO = "Waunakee Airpark <fly@waunakeeairport.com>"
RUNWAY_AGREEMENT_SIGNUP_SEND_EMAIL_TO = "Waunakee Airpark <fly@waunakeeairport.com>"
AOA_FORM_SUBMISSION_SEND_EMAIL_TO = "Waunakee Airpark <fly@waunakeeairport.com>"

EMAIL_CONFIG = env.email_url("EMAIL_URL", default="smtp://@localhost:1025")
vars().update(EMAIL_CONFIG)

ADMINS = [
    ("Dan Silvers", "waunakeeairport@silvers.net"),
]

MANAGERS = [
    ("Dan Silvers", "waunakeeairport@silvers.net"),
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True


CSRF_TRUSTED_ORIGINS = ["https://www.waunakeeairpark.com", "http://localhost:8000", "http://127.0.0.1:8000"]
