"""
Django settings for social_media_api project.
Production-ready version for deployment on Heroku.
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()

# ------------------------------------------------
# BASE DIRECTORY
# ------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------
# SECURITY SETTINGS
# ------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-qw7@auo#vd+z@0$vn191@(a=s)2kh*zc9x_ttmh-cvhnnceqz9')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# For Heroku or other production hosts
ALLOWED_HOSTS = ['*']

# ------------------------------------------------
# APPLICATIONS
# ------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
    'posts',
    'notifications',
]

# ------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Whitenoise middleware for serving static files in production
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------
# URLS AND WSGI
# ------------------------------------------------
ROOT_URLCONF = 'social_media_api.urls'
WSGI_APPLICATION = 'social_media_api.wsgi.application'

# ------------------------------------------------
# TEMPLATES
# ------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------
# Use DATABASE_URL if available (Heroku sets this automatically)
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False
    )
}

# ------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------
# STATIC FILES CONFIGURATION
# ------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Enable Whitenoise compressed storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ------------------------------------------------
# SECURITY HEADERS
# ------------------------------------------------
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True

# ------------------------------------------------
# DJANGO REST FRAMEWORK SETTINGS
# ------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
    ],
}

# ------------------------------------------------
# CUSTOM USER MODEL
# ------------------------------------------------
AUTH_USER_MODEL = 'accounts.CustomUser'
SITE_ID = 1

# ------------------------------------------------
# DEFAULT AUTO FIELD
# ------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
