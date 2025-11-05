"""
WSGI config for bythepong_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Use production settings on Vercel
if os.environ.get('VERCEL'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bythepong_web.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bythepong_web.settings')

application = get_wsgi_application()

# Vercel requires 'app' variable
app = application
