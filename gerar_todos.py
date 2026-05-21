#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GERADOR DE TIMELAPSES PARA TODAS AS 56 CIDADES
Processa todas as cidades com seus dados de satélite de Documents
"""

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
logging.basicConfig(level=logging.ERROR, format='%(message)s')
logger = logging.getLogger(__name__)

from mapa_crescimento import MapaCrescimento

def encontrar_melhor_match(nome_cidade, docs_path):
    """Encontra melhor pasta correspondente à cidade com fuzzy matching"""
    try:
        pastas = []
        for pasta in docs_path.iterdir():
            if not pasta.is_dir():
                continue
            tif_count = len(list(pasta.glob('**/*.tif')))
            if tif_count > 0:
                pastas.append((pasta, tif_count))
        
        if not pastas:
            return None
        
        melhor = None
        melhor_score = 0.0
        cidade_clean = nome_cidade.lower().replace(' ', '_').replace('ã', 'a').replace('õ', 'o')
        
        for pasta, _ in pastas:
            pasta_clean = pasta.name.lower().replace(' ', '_').replace('ã', 'a').replace('õ', 'o')
            
            for sufixo in ['_noturna', '_noturno', '_recorte', '_recortes', '_recortado', '_reprojetado']:
                pasta_clean = pasta_clean.replace(sufixo, '')
            
            score = SequenceMatcher(None, cidade_clean, pasta_clean).ratio()
            
            if score > melhor_score:
                melhor_score = score
                melhor = pasta
        
        return melhor if melhor and melhor_score > 0.5 else None
    except:
        return None

def main():
    inicio_total = time.time()
    
    # Carregar coordenadas
    coords_file = Path(__file__).parent / 'data' / 'coordenadas' / 'coordenadas_cidades_completas_nominatim.json'
    with open(coords_file, 'r', encoding='utf-8') as f:
        cidades = json.load(f)
    
    docs_path = Path.home() / 'Documents'
    mapa = MapaCrescimento()
    mapa.carregar_coordenadas(str(coords_file))
    
    total = len(cidades)
    sucesso = 0
    encontradas = 0
    falhas = []
    tempos = []
    
    print(f"\n{'='*110}")
    print(f"🎬 GERAÇÃO DE TIMELAPSES - TODAS AS {total} CIDADES COM MAPA DE CRESCIMENTO")
    print(f"{'='*110}\n")
    
    for i, nome_cidade in enumerate(sorted(cidades.keys()), 1):
        try:
            pct = (i * 100) // total
            barra = f"[{'█' * (pct//5)}{' ' * (20-pct//5)}] {pct:3d}%"
            
            pasta = encontrar_melhor_match(nome_cidade, docs_path)
            
            if not pasta:
                print(f"{barra} [{i:2d}/{total}] ⏭️  {nome_cidade:40s} ❌")
                falhas.append(nome_cidade)
                continue
            
            encontradas += 1
            print(f"{barra} [{i:2d}/{total}] 🔄 {nome_cidade:40s} ", end='', flush=True)
            
            inicio_cidade = time.time()
            try:
                resultado = mapa.gerar_timelapse_cidade(nome_cidade, str(pasta))
                tempo = time.time() - inicio_cidade
                tempos.append(tempo)
                
                if resultado:
                    arquivo = Path(resultado)
                    tam = arquivo.stat().st_size / 1024 / 1024
                    print(f"✅ {tam:6.1f}MB {tempo:5.0f}s")
                    sucesso += 1
                else:
                    print(f"⚠️  erro")
                    falhas.append(f"{nome_cidade} (geração)")
            except Exception as e:
                print(f"❌ {str(e)[:35]}")
                falhas.append(f"{nome_cidade} (erro)")
                
        except Exception as e:
            print(f"❌ {str(e)[:40]}")
            falhas.append(f"{nome_cidade} (exceção)")
    
    tempo_total = time.time() - inicio_total
    tempo_medio = sum(tempos) / len(tempos) if tempos else 0
    
    print(f"\n{'='*110}")
    print(f"📊 RESULTADO FINAL - {int(tempo_total)}s total ({tempo_medio:.0f}s por timelapse)")
    print(f"{'='*110}")
    print(f"✅ Sucesso:       {sucesso:2d}/{total} ({sucesso*100//total:2d}%)")
    print(f"🔍 Encontradas:   {encontradas:2d}/{total} ({encontradas*100//total:2d}%)")
    print(f"❌ Sem dados:     {total - encontradas:2d}/{total} ({(total-encontradas)*100//total:2d}%)")
    
    if sucesso > 0:
        print(f"\n🎉 SUCESSO! {sucesso} TIMELAPSES GERADOS!")
        print(f"📂 Localização: outputs/timelapse_*.html")
        print(f"🌐 Índice:      outputs/INDEX_CRESCIMENTO.html")
    
    if falhas and len(falhas) <= 30:
        print(f"\n⏭️  Cidades sem dados em Documents ({len(falhas)}):")
        for cidade in sorted(set(f.split('(')[0].strip() for f in falhas)):
            print(f"   - {cidade}")
    elif len(falhas) > 30:
        print(f"\n⏭️  {len(falhas)} cidades sem dados em Documents")
        for cidade in sorted(set(f.split('(')[0].strip() for f in falhas))[:15]:
            print(f"   - {cidade}")
        print(f"   ... e mais {len(falhas) - 15}")
    
    print(f"\n{'='*110}\n")
    
    return sucesso, total

if __name__ == '__main__':
    sucesso, total = main()
    sys.exit(0 if sucesso > 0 else 1)
