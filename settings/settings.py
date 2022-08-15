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

AWS_REGION = env("AWS_DEFAULT_REGION")

CSRF_TRUSTED_ORIGINS = [".waunakeeairpark.com"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'wagtail.contrib.modeladmin',
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",

    # "debug_toolbar",

    "taggit",
    "modelcluster",
    "localflavor",
    "content",
    "documents",
    "timeline",
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
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

    # "debug_toolbar.middleware.DebugToolbarMiddleware",
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
WAGTAILIMAGES_IMAGE_MODEL = 'timeline.WaunakeeImage'
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 20 * 1024 * 1024 
WAGTAILIMAGES_INDEX_PAGE_SIZE = 100

S3_BUCKET_NAME = env("S3_STATIC_FILES_BUCKET", default=None)

if S3_BUCKET_NAME:
    # Production
    # Static files on S3
    # Use `manage.py collectstatic` to sync and upload.
    AWS_QUERYSTRING_AUTH = False
    AWS_STORAGE_BUCKET_NAME = S3_BUCKET_NAME
    AWS_S3_REGION_NAME = AWS_REGION
    AWS_S3_BUCKET_NAME_STATIC = S3_BUCKET_NAME

    STATIC_URL = "https://www.waunakeeairport.com/"
    STATICFILES_DIRS = [os.path.join(ROOT_DIR, "static")]

    # S3 MEDIA FILES IN SUBDIRECTORIES
    # https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
    STATICFILES_LOCATION = "static"
    STATICFILES_STORAGE = "settings.storages.StaticStorage"

    MEDIAFILES_LOCATION = "media"
    DEFAULT_FILE_STORAGE = "settings.storages.MediaStorage"
else:
    # Local Development
    STATIC_URL = "/static/"
    STATICFILES_DIRS = [os.path.join(ROOT_DIR, "static")]

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(ROOT_DIR, "media")

DATABASES = {
    "default": env.db("DATABASE_URL"),
}


# SNS Topic for processing runway agreement form submissions
SNS_TOPIC_AIRPORT_RUNWAY_AGREEMENT = env("SNS_TOPIC_AIRPORT_RUNWAY_AGREEMENT", default=None)
S3_BUCKET_AIRPORT_RUNWAY_AGREEMENT = env("S3_BUCKET_AIRPORT_RUNWAY_AGREEMENT", default=None)

SERVER_EMAIL = "Waunakee Airpark <fly@waunakeeairport.com>"

WAPA_SIGNUP_SEND_EMAIL_TO = "Waunakee Airpark <fly@waunakeeairport.com>"
RUNWAY_AGREEMENT_SIGNUP_SEND_EMAIL_TO = "Waunakee Airpark <fly@waunakeeairport.com>"

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

"""
LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}
"""
