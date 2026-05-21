#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import time
from pathlib import Path
from datetime import datetime
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

# Adicionar paths
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'mapas'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'processamento'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'analise'))

import logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

from mapa_crescimento import MapaCrescimento

def main():
    inicio = time.time()
    
    # Carregar cidades
    coordenadas_file = Path(__file__).parent / 'data' / 'coordenadas' / 'coordenadas_cidades_completas_nominatim.json'
    with open(coordenadas_file, 'r', encoding='utf-8') as f:
        cidades = json.load(f)
    
    mapa = MapaCrescimento()
    total = len(cidades)
    sucesso = 0
    falhas = []
    
    print(f"\n{'='*80}")
    print(f"🚀 GERAÇÃO DE TIMELAPSES COM MAPA DE CRESCIMENTO - TODAS AS 56 CIDADES")
    print(f"{'='*80}\n")
    
    for i, (nome_cidade, coord) in enumerate(cidades.items(), 1):
        try:
            # Mostrar progresso
            pct = (i * 100) // total
            barra = f"[{'█' * (pct//5)}{' ' * (20-pct//5)}]"
            print(f"{barra} {pct:3d}% [{i:2d}/{total}] 🔄 {nome_cidade:40s} ", end='', flush=True)
            
            inicio_cidade = time.time()
            resultado = mapa.gerar_timelapse_cidade(nome_cidade, coord)
            tempo_cidade = time.time() - inicio_cidade
            
            if resultado:
                arquivo = Path(resultado)
                tamanho_mb = arquivo.stat().st_size / 1024 / 1024
                print(f"✅ ({tamanho_mb:.1f} MB, {tempo_cidade:.1f}s)")
                sucesso += 1
            else:
                print(f"⏭️  (pulado - sem dados)")
                falhas.append((nome_cidade, "sem dados"))
                
        except Exception as e:
            print(f"❌ ({str(e)[:30]})")
            falhas.append((nome_cidade, str(e)[:50]))
    
    tempo_total = time.time() - inicio
    
    print(f"\n{'='*80}")
    print(f"📊 RESULTADO FINAL:")
    print(f"{'='*80}")
    print(f"   ✅ Sucesso: {sucesso}/{total} ({sucesso*100//total}%)")
    print(f"   ⏭️  Puladas: {len(falhas)}/{total}")
    print(f"   ⏱️  Tempo total: {tempo_total:.1f}s")
    
    if sucesso > 0:
        print(f"\n✨ TIMELAPSES GERADOS COM SUCESSO!")
        print(f"📁 Localização: outputs/timelapse_*.html")
        print(f"🌐 Abra: outputs/INDEX_CRESCIMENTO.html")
    
    if falhas:
        print(f"\n⚠️  Cidades sem dados ou com erro:")
        for cidade, motivo in falhas[:10]:
            print(f"   - {cidade}: {motivo}")
        if len(falhas) > 10:
            print(f"   ... e mais {len(falhas) - 10}")
    
    print(f"\n{'='*80}\n")

if __name__ == '__main__':
    main()
