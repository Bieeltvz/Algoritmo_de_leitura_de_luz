#!/usr/bin/env python3
"""
Reprocessamento forçado com logging detalhado
"""

import sys
import os
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
import shutil

print("=" * 70)
print("LIMPEZA COMPLETA E REPROCESSAMENTO")
print("=" * 70)

# Deletar arquivos antigos
print("\n1. Removendo arquivos antigos...")
files_to_remove = [
    'processados_Canelinha_recortes.json',
    'resultados_Canelinha_recortes.csv',
    '__pycache__'
]

for f in files_to_remove:
    path = Path(f)
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
            print(f"   Removido: {f}/ (diretorio)")
        else:
            path.unlink()
            print(f"   Removido: {f}")
    else:
        print(f"   Nao encontrado: {f}")

print("\n2. Encontrando pasta de Canelinha...")
docs = Path(r"C:\Users\gtvargas\Documents")
canelinha_pasta = None

for item in docs.iterdir():
    if item.is_dir() and 'canelinha' in item.name.lower() and 'noturna' in item.name.lower():
        canelinha_pasta = item
        break

if not canelinha_pasta:
    print("ERRO: Pasta nao encontrada!")
    exit(1)

raster_dir = canelinha_pasta / "Raster"
recorte_dir = None
for item in raster_dir.iterdir():
    if item.is_dir() and 'recorte' in item.name.lower():
        recorte_dir = item
        break

if not recorte_dir:
    print("ERRO: Pasta de recorte nao encontrada!")
    exit(1)

print(f"   Pasta: {recorte_dir}")

print("\n3. Reprocessando...")
print("=" * 70)

from processador_paralelo import ProcessadorParalelo

# Processar com forcar_reprocessamento=True
processador = ProcessadorParalelo(
    workers=None,
    nome_cidade=recorte_dir.name,
    forcar_reprocessamento=True
)

#Adicionar debug
print(f"\n   ProcessadorParalelo inicializado:")
print(f"   - Nome cidade: {processador.nome_cidade}")
print(f"   - Arquivo resultados: {processador.ARQUIVO_RESULTADOS}")
print(f"   - Workers: {processador.workers}")
print()

processador.processar_pasta(str(recorte_dir))

print("=" * 70)
print("\n4. Verificando resultados...")

import csv
if processador.ARQUIVO_RESULTADOS.exists():
    with open(processador.ARQUIVO_RESULTADOS) as f:
        rows = list(csv.DictReader(f))
        print(f"   Total de registros: {len(rows)}")
        if rows:
            print(f"   Primeiro: media={rows[0]['intensidade_media']}")
            print(f"   Ultimo: media={rows[-1]['intensidade_media']}")
            print(f"   Amostra de 5 valores: {[r['intensidade_media'] for r in rows[::len(rows)//5]]}")
else:
    print(f"   ERRO: Arquivo nao foi criado!")

print("\nCONCLUIDO!")
