"""
Django settings for conf project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "24&j7yo7)tm=l2v(&4b5349$*8y6elu8^7c(v0tb3a7seg^%5e"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)
DEBUG_TOOLBAR = config("DEBUG_TOOLBAR", default=DEBUG, cast=bool)
LOCAL_ENV = config("LOCAL_ENV", default=True, cast=bool)

ALLOWED_HOSTS = ["*"]

if DEBUG_TOOLBAR:
    INTERNAL_IPS = type(str("c"), (), {"__contains__": lambda *a: True})()

# Application definition

INSTALLED_APPS = [
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "collectfast",
    "django.contrib.staticfiles",
    # third-party apps
    "rest_framework",
    "django_q",
    "widget_tweaks",
    "easy_thumbnails",
    "django_filters",
    "ckeditor",
    "debug_toolbar",
    "factory_generator",
    "corsheaders",
    # my apps
    "apps.main",
    "apps.user",
]

AUTH_USER_MODEL = "user.User"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
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

WSGI_APPLICATION = "conf.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static_collected")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

####
# STORAGES
###

COLLECTFAST_ENABLED = False

if not LOCAL_ENV:

    AWS_QUERYSTRING_AUTH = False

    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", None)
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", None)
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }

    COLLECTFAST_ENABLED = True

    STATICFILES_STORAGE = "conf.storage_backends.StaticStorage"
    DEFAULT_FILE_STORAGE = "conf.storage_backends.PublicMediaStorage"
    COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"

    AWS_LOCATION = config("AWS_LOCATION", "")

    AWS_STATIC_LOCATION = f"{AWS_LOCATION}static/"
    AWS_PUBLIC_MEDIA_LOCATION = f"{AWS_LOCATION}media/"
    AWS_PRIVATE_MEDIA_LOCATION = f"{AWS_LOCATION}private/"


####
# JWT
###

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "COERCE_DECIMAL_TO_STRING": False,
}

JWT_AUTH = {
    "JWT_VERIFY_EXPIRATION": False,
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 8000

# Email


DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@test.com")
EMAIL_HOST = config("EMAIL_HOST", default="mail")
EMAIL_PORT = config("EMAIL_PORT", default=1025, cast=int)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="", cast=str)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="", cast=str)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)


####
# CLUSTER
###

Q_CLUSTER = {
    "name": "cluster",
    "workers": 2,
    "timeout": None,
    "django_redis": "default",
}


####
# CACHES
###

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{0}:{1}/{2}".format(
            config("REDIS_HOST"), config("REDIS_PORT"), config("REDIS_DB", default=0)
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": config('REDIS_PASSWORD'),
        },
        "KEY_PREFIX": "django_orm",
    }
}


####
# THUMBNAILS
###

THUMBNAIL_ALIASES = {
    "": {
        "default": {"size": (300, 300), "crop": True},
    },
}


####
# EMAIL
###

EMAIL_FROM = config("EMAIL_FROM", default="test@test.com")

# FACTORY GENERATE

FACTORY_ONLY_APPS = [
    "main",
    "user",
]

FACTORY_IGNORE_INIT_IMPORT = True

# Django Cors
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = False