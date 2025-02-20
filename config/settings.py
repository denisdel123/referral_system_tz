"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from core import constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = constants.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = constants.DEBUG

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_spectacular',
    'users',
    'rest_framework_simplejwt',
    'django_celery_beat',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': constants.POSTGRES_DB,
            'USER': constants.POSTGRES_USER,
            'PASSWORD': constants.POSTGRES_PASSWORD,
            'HOST': constants.DB_HOST,
            'PORT': constants.DB_PORT,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API Реферальной системы",
    "DESCRIPTION": "позволяет регистрироваться с помощью рефералов а так же отправлять письма на почту пользователя",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,  # Не включаем схему внутрь документации
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },
    "SECURITY": [{"Bearer": []}],
}

# Настройка пользователя
AUTH_USER_MODEL = "users.User"

# JWT-token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Время жизни access-токена
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Время жизни refresh-токена
    'ROTATE_REFRESH_TOKENS': True,  # Обновлять refresh-токен при каждом обновлении access-токена
    'BLACKLIST_AFTER_ROTATION': True,  # Деактивировать старый refresh-токен после обновления
    'ALGORITHM': 'HS256',  # Алгоритм шифрования
    'SIGNING_KEY': 'your-secret-key',  # Ключ подписи (лучше загружать из переменных окружения)
}


CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TIMEZONE = "Europe/Moscow"

# Настройка почты
EMAIL_BACKEND = constants.EMAIL_BACKEND
EMAIL_HOST = constants.EMAIL_HOST
EMAIL_PORT = constants.EMAIL_PORT
EMAIL_USE_TLS = constants.EMAIL_USE_TLS
EMAIL_HOST_USER = constants.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = constants.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
