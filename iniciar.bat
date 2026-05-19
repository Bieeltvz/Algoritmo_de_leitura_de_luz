@echo off
REM Iniciar Flask com encoding UTF-8 correto
cd /d "%~dp0"
setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║  🚀 Iniciando Aplicação de Leitura de Luz                   ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Configurar encoding UTF-8
chcp 65001 >nul

REM Definir variável de ambiente
set PYTHONIOENCODING=utf-8

REM Navegar para app/
cd app

echo ✅ Iniciando Flask...
echo 📍 Acesse: http://localhost:5000
echo.
echo 🔴 Pressione Ctrl+C para parar o servidor
echo.

python app.py

pause
