#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🚀 Script de inicialização da aplicação
Inicia o Flask com configuração correta de encoding e paths
"""

import os
import sys
import subprocess
from pathlib import Path

# Configurar encoding UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Diretório do projeto
PROJECT_DIR = Path(__file__).parent
APP_DIR = PROJECT_DIR / 'app'

# Configurar sys.path
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'processamento'))
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'mapas'))
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'analise'))
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'utils'))
sys.path.insert(0, str(PROJECT_DIR / 'src'))

print()
print("╔═══════════════════════════════════════════════════════════════╗")
print("║  🚀 Algoritmo de Leitura de Luz de Satélite                  ║")
print("║     Interface Web Flask                                       ║")
print("╚═══════════════════════════════════════════════════════════════╝")
print()

print("✅ Verificando dependências...")

# Verificar se templates e static existem
templates_path = APP_DIR / 'templates' / 'index.html'
static_path = APP_DIR / 'static' / 'script.js'

checks = [
    (templates_path.exists(), f"✅ Templates: {templates_path}"),
    (static_path.exists(), f"✅ Static: {static_path}"),
]

all_good = True
for check, msg in checks:
    if check:
        print(msg)
    else:
        print(msg.replace('✅', '❌'))
        all_good = False

if not all_good:
    print()
    print("❌ Alguns arquivos estão faltando!")
    print("   Execute de: " + str(PROJECT_DIR))
    sys.exit(1)

print()
print("📍 Acesse: http://localhost:5000")
print("🔴 Pressione Ctrl+C para parar o servidor")
print()

# Mudar para diretório de app e executar
os.chdir(APP_DIR)

print("⏳ Aguarde alguns segundos para inicializar...")
print()

try:
    # Executar app.py com subprocess
    process = subprocess.Popen(
        [sys.executable, 'app.py'],
        env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
    )
    process.wait()
except KeyboardInterrupt:
    print()
    print("⏹️  Servidor parado.")
    sys.exit(0)
except Exception as e:
    print(f"❌ Erro ao iniciar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
