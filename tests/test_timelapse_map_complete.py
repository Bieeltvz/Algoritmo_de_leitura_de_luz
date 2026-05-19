#!/usr/bin/env python3
"""
Teste completo: Timelapse + Mapa interativo para Braco Do Trombudo
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento
import logging
import sys
import io
import os

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Mudar para diretório correto
DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
os.chdir(DIRETORIO_TRABALHO)

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

mapa = MapaCrescimento()

print("=" * 70)
print("TESTE COMPLETO: Timelapse + Mapa para Braco Do Trombudo")
print("=" * 70)
print(f"Diretório de trabalho: {DIRETORIO_TRABALHO}")

nome_cidade = "Braco_Do_Trombudo_recortes"

# Carregar coordenadas primeiro
print(f"\n[0] Carregando coordenadas...")
if not mapa.carregar_coordenadas():
    print(f"    ❌ Falha ao carregar coordenadas")
    sys.exit(1)
print(f"    ✅ {len(mapa.coordenadas)} cidades carregadas")

# 1. Gerar Timelapse
print(f"\n[1] Gerando Timelapse para {nome_cidade}...")
arquivo_timelapse = DIRETORIO_TRABALHO / f'timelapse_{nome_cidade}_test.html'
resultado_timelapse = mapa.gerar_timelapse_cidade(nome_cidade, str(arquivo_timelapse))

if resultado_timelapse and Path(resultado_timelapse).exists():
    tamanho_timelapse = Path(resultado_timelapse).stat().st_size / 1024 / 1024
    print(f"    ✅ Timelapse gerado: {tamanho_timelapse:.1f} MB")
else:
    print(f"    ❌ Falha na geração do timelapse")
    sys.exit(1)

# 2. Gerar Mapa
print(f"\n[2] Gerando Mapa Interativo para {nome_cidade}...")
arquivo_mapa = DIRETORIO_TRABALHO / f'mapa_{nome_cidade}_test.html'
resultado_mapa = mapa.gerar_relatorio_html_cidade(nome_cidade, str(arquivo_mapa))

if resultado_mapa and Path(resultado_mapa).exists():
    tamanho_mapa = Path(resultado_mapa).stat().st_size / 1024
    print(f"    ✅ Mapa gerado: {tamanho_mapa:.1f} KB")
else:
    print(f"    ❌ Falha na geração do mapa")
    sys.exit(1)

# 3. Resumo
print("\n" + "=" * 70)
print("RESULTADO FINAL")
print("=" * 70)
print(f"✅ Timelapse: {resultado_timelapse}")
print(f"✅ Mapa: {resultado_mapa}")
print("\n✅ TODOS OS TESTES PASSARAM!")
print("=" * 70)
