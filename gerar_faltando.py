#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from pathlib import Path
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

# Adicionar paths
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'mapas'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'processamento'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'analise'))

import logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from mapa_crescimento import MapaCrescimento

def main():
    # Carregar cidades
    coordenadas_file = Path(__file__).parent / 'data' / 'coordenadas' / 'coordenadas_cidades_completas_nominatim.json'
    with open(coordenadas_file, 'r', encoding='utf-8') as f:
        cidades = json.load(f)
    
    # Cidades já geradas
    outputs_dir = Path(__file__).parent / 'outputs'
    cidades_geradas = set()
    for html_file in outputs_dir.glob('timelapse_*.html'):
        # Extrair nome da cidade do arquivo
        nome = html_file.stem.replace('timelapse_', '').replace('_debug', '')
        cidades_geradas.add(nome)
    
    mapa = MapaCrescimento()
    total = len(cidades)
    sucesso = 0
    pendentes = []
    
    print(f"\n{'='*70}")
    print(f"🚀 GERAÇÃO DE TIMELAPSES COM MAPA DE CRESCIMENTO")
    print(f"{'='*70}")
    print(f"Total de cidades: {total}")
    print(f"Já geradas: {len(cidades_geradas)}")
    print(f"Pendentes: {total - len(cidades_geradas)}")
    print(f"{'='*70}\n")
    
    for i, (nome_cidade, coord) in enumerate(cidades.items(), 1):
        try:
            # Verificar se já foi gerada
            if nome_cidade in cidades_geradas or any(nome_cidade.lower() in g.lower() for g in cidades_geradas):
                print(f"[{i:2d}/{total}] ⏭️  {nome_cidade:40s} (já gerada)")
                sucesso += 1
                continue
            
            # Gerar timelapse
            print(f"[{i:2d}/{total}] 🔄 {nome_cidade:40s} ", end='', flush=True)
            resultado = mapa.gerar_timelapse_cidade(nome_cidade, coord)
            
            if resultado:
                arquivo = Path(resultado).name
                tamanho_mb = Path(resultado).stat().st_size / 1024 / 1024
                print(f"✅ ({tamanho_mb:.1f} MB)")
                sucesso += 1
            else:
                print(f"⚠️ (sem dados)")
                pendentes.append(nome_cidade)
                
        except Exception as e:
            print(f"❌ ({str(e)[:30]})")
            pendentes.append(nome_cidade)
    
    print(f"\n{'='*70}")
    print(f"📊 RESULTADO:")
    print(f"   ✅ Geradas: {sucesso}/{total}")
    print(f"   ⏭️  Pendentes: {total - sucesso}/{total}")
    
    if pendentes:
        print(f"\n❌ Cidades sem dados:")
        for cidade in sorted(pendentes)[:15]:
            print(f"   - {cidade}")
        if len(pendentes) > 15:
            print(f"   ... e mais {len(pendentes) - 15}")
    
    print(f"\n✨ Taxa: {sucesso*100//total}%")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    main()
