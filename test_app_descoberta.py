#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste que importa a função descobrir_pastas_cidades do app.py
"""

import sys
from pathlib import Path

# Adicionar o diretório atual ao path para importar app
sys.path.insert(0, str(Path(__file__).parent))

# Importar a função do app.py
from app import descobrir_pastas_cidades

print("=" * 100)
print("SIMULANDO DESCOBERTA AUTOMÁTICA (importando do app.py)")
print("=" * 100)

pastas = descobrir_pastas_cidades()

print(f"\nTotal de pastas descobertas: {len(pastas)}")

# Procurar especificamente por Balneário
print("\n" + "=" * 100)
print("PROCURANDO BALNEÁRIO:")
print("=" * 100)

balneario_encontradas = [info for info in pastas.values() if 'balneario' in info['cidade'].lower()]

if balneario_encontradas:
    print(f"\n✓ Encontradas {len(balneario_encontradas)} entradas com 'Balneário':")
    for i, info in enumerate(balneario_encontradas, 1):
        print(f"  {i}. {info['nome_amigavel']}")
        print(f"     Chave: {info['nome']}")
        print(f"     Cidade: {info['cidade']}")
        print(f"     Tipo recorte: {info['tipo_recorte']}")
else:
    print("\n✗ NENHUMA entrada com 'Balneário' encontrada!")
