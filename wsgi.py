import os
from django.core.wsgi import get_wsgi_application

# Usar configuração minimal para Vercel
if os.environ.get('VERCEL'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bythepong_web.settings_minimal')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bythepong_web.settings')

application = get_wsgi_application()
