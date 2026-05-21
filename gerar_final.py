#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import time
from pathlib import Path
from difflib import SequenceMatcher
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, str(Path(__file__).parent / 'src' / 'mapas'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'processamento'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'analise'))

import logging
logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger(__name__)

from mapa_crescimento import MapaCrescimento

def encontrar_melhor_match_pasta(nome_cidade, docs_path):
    """Encontra a pasta que melhor corresponde ao nome da cidade"""
    pastas_candidatas = []
    for pasta in docs_path.iterdir():
        if not pasta.is_dir():
            continue
        tif_count = len(list(pasta.glob('**/*.tif')))
        if tif_count > 0:
            pastas_candidatas.append((pasta, tif_count))
    
    if not pastas_candidatas:
        return None
    
    melhor_pasta = None
    melhor_score = 0.0
    nome_cidade_clean = nome_cidade.lower().replace(' ', '_').replace('ã', 'a').replace('õ', 'o')
    
    for pasta, _ in pastas_candidatas:
        pasta_clean = pasta.name.lower().replace(' ', '_').replace('ã', 'a').replace('õ', 'o')
        
        for sufixo in ['_noturna', '_noturno', '_recorte', '_recortes', '_recortado', '_reprojetado']:
            pasta_clean = pasta_clean.replace(sufixo, '')
        
        score = SequenceMatcher(None, nome_cidade_clean, pasta_clean).ratio()
        
        if score > melhor_score:
            melhor_score = score
            melhor_pasta = pasta
    
    if melhor_pasta and melhor_score > 0.5:
        return melhor_pasta
    
    return None

def main():
    inicio = time.time()
    
    # Carregar coordenadas
    coordenadas_file = Path(__file__).parent / 'data' / 'coordenadas' / 'coordenadas_cidades_completas_nominatim.json'
    with open(coordenadas_file, 'r', encoding='utf-8') as f:
        cidades_coords = json.load(f)
    
    docs_path = Path.home() / 'Documents'
    mapa = MapaCrescimento()
    
    # Carregar coordenadas no mapa
    mapa.carregar_coordenadas(str(coordenadas_file))
    
    total = len(cidades_coords)
    sucesso = 0
    encontradas = 0
    falhas = []
    
    print(f"\n{'='*100}")
    print(f"🚀 GERANDO {total} TIMELAPSES COM MAPA DE CRESCIMENTO")
    print(f"{'='*100}\n")
    
    for i, nome_cidade in enumerate(sorted(cidades_coords.keys()), 1):
        try:
            # Mostrar progresso
            pct = (i * 100) // total
            barra = f"[{'█' * (pct//5)}{' ' * (20-pct//5)}] {pct:3d}%"
            
            # Procurar pasta
            pasta_cidade = encontrar_melhor_match_pasta(nome_cidade, docs_path)
            
            if not pasta_cidade:
                print(f"{barra} [{i:2d}/{total}] ⏭️  {nome_cidade:38s} ❌ sem dados")
                falhas.append(nome_cidade)
                continue
            
            encontradas += 1
            tif_count = len(list(pasta_cidade.glob('**/*.tif')))
            
            print(f"{barra} [{i:2d}/{total}] 🔄 {nome_cidade:38s} ", end='', flush=True)
            
            inicio_cidade = time.time()
            resultado = mapa.gerar_timelapse_cidade(nome_cidade, str(pasta_cidade))
            tempo_cidade = time.time() - inicio_cidade
            
            if resultado:
                arquivo = Path(resultado)
                tamanho_mb = arquivo.stat().st_size / 1024 / 1024
                print(f"✅ {tamanho_mb:6.1f}MB ({tempo_cidade:4.0f}s, {tif_count:3d} tifs)")
                sucesso += 1
            else:
                print(f"⚠️  erro ao gerar")
                falhas.append(f"{nome_cidade} (erro geração)")
                
        except Exception as e:
            print(f"❌ {str(e)[:40]}")
            falhas.append(f"{nome_cidade} (exceção)")
    
    tempo_total = time.time() - inicio
    
    print(f"\n{'='*100}")
    print(f"📊 RESULTADO FINAL - {int(tempo_total)}s")
    print(f"{'='*100}")
    print(f"✅ Sucesso:       {sucesso:3d}/{total} ({sucesso*100//total:2d}%)")
    print(f"🔍 Encontrados:   {encontradas:3d}/{total} ({encontradas*100//total:2d}%)")
    print(f"❌ Sem dados:     {total - encontradas:3d}/{total} ({(total-encontradas)*100//total:2d}%)")
    
    if sucesso > 0:
        print(f"\n🎉 TIMELAPSES GERADOS!")
        print(f"📂 Pasta: c:\\Users\\gtvargas\\Desktop\\Algoritmo_de_leitura_de_luz\\outputs\\")
        print(f"📄 Arquivos: timelapse_*.html")
        print(f"🌐 Índice: INDEX_CRESCIMENTO.html")
    
    if 0 < len(falhas) <= 25:
        print(f"\n⏭️  Cidades sem dados em Documents:")
        for cidade in sorted(set(f.split('(')[0].strip() for f in falhas)):
            print(f"   - {cidade}")
    elif len(falhas) > 25:
        print(f"\n⏭️  Sem dados: {len(falhas)} cidades (vide logs)")
    
    print(f"\n{'='*100}\n")

if __name__ == '__main__':
    main()
