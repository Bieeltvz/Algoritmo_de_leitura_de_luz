#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import time
from pathlib import Path
from datetime import datetime
import os
from difflib import SequenceMatcher

os.environ['PYTHONIOENCODING'] = 'utf-8'

# Adicionar paths
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'mapas'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'processamento'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'analise'))

import logging
logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger(__name__)

from mapa_crescimento import MapaCrescimento

def encontrar_melhor_match_pasta(nome_cidade, docs_path):
    """Encontra a pasta que melhor corresponde ao nome da cidade usando SequenceMatcher"""
    
    # Carregar lista de pastas com TIF
    pastas_candidatas = []
    for pasta in docs_path.iterdir():
        if not pasta.is_dir():
            continue
        if not list(pasta.glob('**/*.tif')):
            continue
        pastas_candidatas.append(pasta)
    
    if not pastas_candidatas:
        return None
    
    # Encontrar melhor match
    melhor_pasta = None
    melhor_score = 0.0
    
    nome_cidade_clean = nome_cidade.lower().replace(' ', '_')
    
    for pasta in pastas_candidatas:
        pasta_clean = pasta.name.lower()
        
        # Remover sufixos para comparação
        for sufixo in ['_noturna', '_noturno', '_recorte', '_recortes', '_recortado', '_reprojetado']:
            pasta_clean = pasta_clean.replace(sufixo, '')
        
        # Calcular similaridade
        score = SequenceMatcher(None, nome_cidade_clean, pasta_clean).ratio()
        
        if score > melhor_score:
            melhor_score = score
            melhor_pasta = pasta
    
    # Retornar se score > 0.6 (60% de similaridade)
    if melhor_pasta and melhor_score > 0.6:
        return melhor_pasta
    
    return None

def main():
    inicio = time.time()
    
    # Carregar cidades
    coordenadas_file = Path(__file__).parent / 'data' / 'coordenadas' / 'coordenadas_cidades_completas_nominatim.json'
    with open(coordenadas_file, 'r', encoding='utf-8') as f:
        cidades = json.load(f)
    
    docs_path = Path.home() / 'Documents'
    
    mapa = MapaCrescimento()
    total = len(cidades)
    sucesso = 0
    encontradas = 0
    falhas = []
    
    print(f"\n{'='*90}")
    print(f"🚀 GERANDO TIMELAPSES - TODAS AS 56 CIDADES")
    print(f"📂 Buscando dados em: {docs_path}")
    print(f"{'='*90}\n")
    
    for i, (nome_cidade, coord) in enumerate(cidades.items(), 1):
        try:
            pct = (i * 100) // total
            barra = f"[{'█' * (pct//5)}{' ' * (20-pct//5)}]"
            
            # Procurar pasta com fuzzy matching
            pasta_cidade = encontrar_melhor_match_pasta(nome_cidade, docs_path)
            
            if not pasta_cidade:
                print(f"{barra} {pct:3d}% [{i:2d}/{total}] ⏭️  {nome_cidade:35s} (sem dados)")
                falhas.append((nome_cidade, "sem dados"))
                continue
            
            encontradas += 1
            print(f"{barra} {pct:3d}% [{i:2d}/{total}] 🔄 {nome_cidade:35s} ", end='', flush=True)
            
            inicio_cidade = time.time()
            
            try:
                resultado = mapa.gerar_timelapse_cidade(nome_cidade, str(pasta_cidade))
                tempo_cidade = time.time() - inicio_cidade
                
                if resultado:
                    arquivo = Path(resultado)
                    tamanho_mb = arquivo.stat().st_size / 1024 / 1024
                    print(f"✅ ({tamanho_mb:.1f}MB, {tempo_cidade:.0f}s)")
                    sucesso += 1
                else:
                    print(f"❌ (erro ao gerar)")
                    falhas.append((nome_cidade, "erro ao gerar"))
            except Exception as e:
                print(f"❌ ({str(e)[:30]})")
                falhas.append((nome_cidade, str(e)[:40]))
                
        except Exception as e:
            print(f"❌ erro: {str(e)[:40]}")
            falhas.append((nome_cidade, str(e)[:40]))
    
    tempo_total = time.time() - inicio
    
    print(f"\n{'='*90}")
    print(f"📊 RESULTADO FINAL")
    print(f"{'='*90}")
    print(f"✅ Sucesso:      {sucesso}/{total} ({sucesso*100//total}%)")
    print(f"🔍 Encontrados:  {encontradas}/{total} ({encontradas*100//total}%)")
    print(f"⏭️  Sem dados:    {total - encontradas}/{total}")
    print(f"⏱️  Tempo total:  {tempo_total:.0f}s")
    
    if sucesso > 0:
        print(f"\n🎉 SUCESSO!")
        print(f"📍 Localização: outputs/timelapse_*.html")
        print(f"🌐 Índice:      outputs/INDEX_CRESCIMENTO.html")
    
    if falhas and len(falhas) <= 20:
        print(f"\n⚠️  Cidades processadas:")
        for cidade, status in falhas:
            print(f"   ⏭️  {cidade}: {status}")
    
    print(f"\n{'='*90}\n")

if __name__ == '__main__':
    main()
