"""
Vercel WSGI Handler
Este arquivo é o ponto de entrada para a Vercel
"""
import os
import sys

# Configurar variável de ambiente ANTES de importar Django
os.environ['VERCEL'] = '1'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bythepong_web.settings_vercel')

try:
    from django.core.wsgi import get_wsgi_application
    # Esta é a variável que a Vercel procura
    app = get_wsgi_application()
except Exception as e:
    # Se houver erro, logar e criar uma resposta de erro básica
    import traceback
    error_trace = traceback.format_exc()
    print(f"ERRO ao inicializar Django: {e}")
    print(error_trace)
    
    def app(environ, start_response):
        """Fallback handler em caso de erro"""
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, response_headers)
        error_msg = f'Erro ao inicializar aplicação: {str(e)}\n\n{error_trace}'
        return [error_msg.encode('utf-8')]

