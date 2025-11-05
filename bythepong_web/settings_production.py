"""
Django settings for production on Vercel with PostgreSQL
"""
import os
import dj_database_url
from .settings import *

# SECURITY
DEBUG = False
ALLOWED_HOSTS = ['.vercel.app', 'bythepong-webb.vercel.app', 'localhost', '127.0.0.1']

# PostgreSQL Database Configuration
if os.environ.get('POSTGRES_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('POSTGRES_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
elif os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback para SQLite em memória se não houver PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

# Static files - WhiteNoise handles this
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = False  # Vercel handles HTTPS
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app', 'https://bythepong-webb.vercel.app']

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
