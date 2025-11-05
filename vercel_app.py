"""
Vercel WSGI Handler
Este arquivo é o ponto de entrada para a Vercel
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bythepong_web.settings_vercel')

from django.core.wsgi import get_wsgi_application

# Esta é a variável que a Vercel procura
app = get_wsgi_application()

