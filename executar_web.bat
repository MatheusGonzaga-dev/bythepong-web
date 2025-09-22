@echo off
title ByThePong Web - Servidor
color 0A

echo.
echo  ========================================
echo   🏓 ByThePong - Versao Web
echo  ========================================
echo   🚀 Iniciando servidor web...
echo   🌐 Sera aberto em: http://localhost:5000
echo  ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado! 
    echo 📥 Baixe em: https://python.org
    pause
    exit /b 1
)

REM Instala dependências se necessário
if not exist venv\ (
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Erro ao instalar dependencias!
        pause
        exit /b 1
    )
)

REM Executa o servidor
echo ✅ Iniciando ByThePong Web...
python executar_web.py

pause

