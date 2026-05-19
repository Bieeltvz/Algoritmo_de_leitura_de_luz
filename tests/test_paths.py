#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se os caminhos estão corretos
"""

from pathlib import Path
import os

# Simular o que app.py faz
DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
os.chdir(DIRETORIO_TRABALHO)

print(f"✓ Diretório de trabalho: {DIRETORIO_TRABALHO}")
print(f"✓ CWD atual: {Path.cwd()}")

# Simular o processador paralelo
nome_cidade = 'Braco_Do_Trombudo_recortes'

# Criar arquivos de teste
arquivo_cache = DIRETORIO_TRABALHO / f'processados_{nome_cidade}.json'
arquivo_csv = DIRETORIO_TRABALHO / f'resultados_{nome_cidade}.csv'

print(f"\nArquivos esperados:")
print(f"  Cache: {arquivo_cache}")
print(f"  CSV: {arquivo_csv}")

# Verificar se os arquivos existem
print(f"\nArquivos existentes:")
print(f"  Cache existe: {arquivo_cache.exists()}")
print(f"  CSV existe: {arquivo_csv.exists()}")

# Listar arquivos CSV no diretório
print(f"\nArquivos CSV no diretório de trabalho:")
for arquivo in DIRETORIO_TRABALHO.glob('resultados_*.csv'):
    print(f"  - {arquivo.name}")

# Listar arquivos JSON no diretório
print(f"\nArquivos JSON no diretório de trabalho:")
for arquivo in DIRETORIO_TRABALHO.glob('processados_*.json'):
    print(f"  - {arquivo.name}")
