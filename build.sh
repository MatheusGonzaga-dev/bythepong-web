#!/bin/bash
# Script para build na Vercel

# Instalar dependências
pip install -r requirements_web.txt

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

echo "Build concluído!"
