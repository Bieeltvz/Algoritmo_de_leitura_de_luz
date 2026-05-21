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

def encontrar_pasta_cidade(nome_cidade):
    """Procura pela pasta da cidade em Documents"""
    docs_path = Path.home() / 'Documents'
    
    # Nomes alternativos
    nomes_para_tentar = [
        nome_cidade,
        nome_cidade.replace(' ', '_'),
        nome_cidade + '_noturna',
        nome_cidade + '_noturno',
        nome_cidade + '_recorte',
        nome_cidade + '_recortes',
        nome_cidade + '_RECORTADO',
    ]
    
    for nome in nomes_para_tentar:
        pasta = docs_path / nome
        if pasta.exists():
            # Verificar se tem imagens TIF
            tifs = list(pasta.glob('**/*.tif'))
            if tifs:
                return pasta
    
    return None

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
    encontradas = 0
    
    print(f"\n{'='*90}")
    print(f"🚀 GERAÇÃO DE TIMELAPSES - TODAS AS 56 CIDADES COM IMAGENS DE SATELLITE")
    print(f"{'='*90}\n")
    
    for i, (nome_cidade, coord) in enumerate(cidades.items(), 1):
        try:
            pct = (i * 100) // total
            barra = f"[{'█' * (pct//5)}{' ' * (20-pct//5)}]"
            
            # Procurar pasta
            pasta_cidade = encontrar_pasta_cidade(nome_cidade)
            
            if not pasta_cidade:
                print(f"{barra} {pct:3d}% [{i:2d}/{total}] ⏭️  {nome_cidade:40s} (pasta não encontrada)")
                falhas.append((nome_cidade, "pasta não encontrada"))
                continue
            
            encontradas += 1
            print(f"{barra} {pct:3d}% [{i:2d}/{total}] 🔄 {nome_cidade:40s} ", end='', flush=True)
            
            inicio_cidade = time.time()
            resultado = mapa.gerar_timelapse_cidade(nome_cidade, str(pasta_cidade))
            tempo_cidade = time.time() - inicio_cidade
            
            if resultado:
                arquivo = Path(resultado)
                tamanho_mb = arquivo.stat().st_size / 1024 / 1024
                print(f"✅ ({tamanho_mb:.1f} MB, {tempo_cidade:.1f}s)")
                sucesso += 1
            else:
                print(f"⚠️  (erro ao gerar)")
                falhas.append((nome_cidade, "erro ao gerar"))
                
        except Exception as e:
            print(f"❌ ({str(e)[:35]})")
            falhas.append((nome_cidade, str(e)[:40]))
    
    tempo_total = time.time() - inicio
    
    print(f"\n{'='*90}")
    print(f"📊 RESULTADO FINAL:")
    print(f"{'='*90}")
    print(f"   ✅ Sucesso:         {sucesso}/{total} ({sucesso*100//total}%)")
    print(f"   🔍 Encontradas:     {encontradas}/{total} ({encontradas*100//total}%)")
    print(f"   ⏭️  Sem pasta/dados: {len(falhas)}/{total}")
    print(f"   ⏱️  Tempo total:     {tempo_total:.1f}s")
    
    if sucesso > 0:
        print(f"\n✨ TIMELAPSES GERADOS COM SUCESSO!")
        print(f"📁 Localização: outputs/timelapse_*.html")
        print(f"🌐 Índice: outputs/INDEX_CRESCIMENTO.html")
    
    if falhas:
        print(f"\n⚠️  Cidades sem pasta/dados:")
        for cidade, motivo in falhas[:15]:
            print(f"   - {cidade}: {motivo}")
        if len(falhas) > 15:
            print(f"   ... e mais {len(falhas) - 15}")
    
    print(f"\n{'='*90}\n")

if __name__ == '__main__':
    main()
