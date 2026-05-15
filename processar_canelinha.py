#!/usr/bin/env python3
"""
Processa Canelinha_recortes com nome correto
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
from processador_paralelo import ProcessadorParalelo
import shutil

# Remover arquivos antigos
print("Limpando arquivos antigos...")
for f in ['resultados_Canelinha_recortes.csv', 'processados_Canelinha_recortes.json']:
    path = Path(f)
    if path.exists():
        path.unlink()
        print(f"  Removido: {f}")

# Limpar cache Python
cache_dir = Path('__pycache__')
if cache_dir.exists():
    shutil.rmtree(cache_dir)
    print("  Removido: __pycache__/")

print("\nProcessando Canelinha_recortes...")
print("=" * 70)

# Caminho correto
pasta_canelinha = Path(r"C:\Users\gtvargas\Documents\Canelinha_noturna\Raster\Canelinha_recortes")

if not pasta_canelinha.exists():
    print(f"ERRO: Pasta nao encontrada: {pasta_canelinha}")
    exit(1)

print(f"Pasta: {pasta_canelinha}")
print(f"Total de arquivos TIFF: {len(list(pasta_canelinha.glob('**/*.tif')))}")

# Processar
processador = ProcessadorParalelo(
    nome_cidade="Canelinha_recortes",
    forcar_reprocessamento=True
)

processador.processar_pasta(str(pasta_canelinha))

print("=" * 70)
print("\nVerificando resultados...")

import csv
csv_file = Path('resultados_Canelinha_recortes.csv')

if csv_file.exists():
    with open(csv_file) as f:
        rows = list(csv.DictReader(f))
        print(f"Total de registros: {len(rows)}")
        print(f"Primeiros 5 valores de media:")
        for i, r in enumerate(rows[:5], 1):
            print(f"  {i}. {r['arquivo']}: media={r['intensidade_media']}")
else:
    print(f"ERRO: Arquivo nao encontrado: {csv_file}")

print("\nConcluido!")
