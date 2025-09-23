import os

# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security
SECRET_KEY = 'django-minimal-vercel-2024'
DEBUG = False
ALLOWED_HOSTS = ['*']

# Minimal apps
INSTALLED_APPS = [
    'django.contrib.staticfiles',
]

# Minimal middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# URLs
ROOT_URLCONF = 'bythepong_web.urls_minimal'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'bythepong_web.wsgi.application'

# No database
DATABASES = {}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = False

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
