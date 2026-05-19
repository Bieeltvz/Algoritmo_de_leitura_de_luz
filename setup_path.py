# -*- coding: utf-8 -*-
"""
setup_path.py
Configura o path do Python para importar módulos da estrutura nova
Execute isto uma única vez ou importe em main.py
"""

import sys
from pathlib import Path

# Adiciona src/ ao path para facilitar imports
PROJECT_DIR = Path(__file__).parent
SRC_DIR = PROJECT_DIR / 'src'

# Adiciona todas as subpastas de src ao path
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(SRC_DIR / 'processamento'))
sys.path.insert(0, str(SRC_DIR / 'mapas'))
sys.path.insert(0, str(SRC_DIR / 'analise'))
sys.path.insert(0, str(SRC_DIR / 'utils'))
sys.path.insert(0, str(SRC_DIR / 'visualizacao'))

print("✅ Path setup concluído")
print(f"   Projeto: {PROJECT_DIR}")
print(f"   Módulos em src/ agora são importáveis")
