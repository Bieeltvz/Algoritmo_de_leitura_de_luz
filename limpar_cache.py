"""
Script para limpar cache e reprocessar Canelinha com os valores convertidos
"""

import json
import sys
import io
from pathlib import Path
import os

# Corrigir encoding no Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("Limpando cache de Canelinha...")
cache_files = [
    'processados_Canelinha_recortes.json',
    'resultados_Canelinha_recortes.csv'
]
for file in cache_files:
    path = Path(file)
    if path.exists():
        os.remove(path)
        print(f"  ✅ Removido: {file}")
    else:
        print(f"  ⏭️  Não encontrado: {file}")

print("\n📂 Detectando pasta de Canelinha...")
docs = Path(r"C:\Users\gtvargas\Documents")
canelinha_pasta = None

# Procurar pasta
for item in docs.iterdir():
    if item.is_dir() and 'canelinha' in item.name.lower() and 'noturna' in item.name.lower():
        canelinha_pasta = item
        break

if not canelinha_pasta:
    print("❌ Pasta Canelinha não encontrada!")
    exit(1)

print(f"✅ Pasta encontrada: {canelinha_pasta.name}")

# Procurar a pasta de recortes
raster_dir = canelinha_pasta / "Raster"
if not raster_dir.exists():
    print(f"❌ Pasta Raster não encontrada!")
    exit(1)

recorte_dir = None
for item in raster_dir.iterdir():
    if item.is_dir() and 'recorte' in item.name.lower():
        recorte_dir = item
        break

if not recorte_dir:
    print(f"❌ Pasta de recorte não encontrada em {raster_dir}!")
    exit(1)

print(f"✅ Pasta de recorte: {recorte_dir.name}")

print(f"\n🚀 Reprocessando {recorte_dir.name}...")
print("=" * 60)

from processador_paralelo import ProcessadorParalelo

try:
    # Passar o nome da cidade/recorte para gerar arquivos específicos
    processador = ProcessadorParalelo(
        workers=None,
        nome_cidade=recorte_dir.name,  # ← Usar o nome da pasta
        forcar_reprocessamento=True     # ← Forçar limpeza do cache
    )
    processador.processar_pasta(str(recorte_dir))
    print("\n" + "=" * 60)
    print("✅ Reprocessamento concluído!")
    print(f"📊 Resultados salvos em: resultados_{recorte_dir.name}.csv")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
