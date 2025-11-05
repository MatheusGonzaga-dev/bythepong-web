#!/bin/bash
# Script de build para Vercel

echo "🔨 Instalando dependências..."
pip install -r requirements_web.txt

echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "✅ Build concluído!"
