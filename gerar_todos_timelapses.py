#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from pathlib import Path

# Configurar encoding
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Adicionar paths
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'mapas'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'processamento'))
sys.path.insert(0, str(Path(__file__).parent / 'src' / 'analise'))

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar módulo
from mapa_crescimento import MapaCrescimento

def main():
    logger.info("🚀 Iniciando geração de timelapses com mapa de crescimento para 56 cidades...")
    
    # Carregar cidades
    coordenadas_file = Path(__file__).parent / 'data' / 'coordenadas' / 'coordenadas_cidades_completas_nominatim.json'
    with open(coordenadas_file, 'r', encoding='utf-8') as f:
        cidades = json.load(f)
    
    mapa = MapaCrescimento()
    total = len(cidades)
    sucesso = 0
    falhas = []
    
    logger.info(f"📍 Total de cidades: {total}")
    logger.info("=" * 60)
    
    for i, (nome_cidade, coord) in enumerate(cidades.items(), 1):
        try:
            logger.info(f"\n[{i:2d}/{total}] 🔄 Processando: {nome_cidade}...")
            
            # Gerar timelapse
            resultado = mapa.gerar_timelapse_cidade(nome_cidade, coord)
            
            if resultado:
                logger.info(f"     ✅ Sucesso! Arquivo: {Path(resultado).name}")
                sucesso += 1
            else:
                logger.warning(f"     ⚠️ Falha ao gerar timelapse")
                falhas.append(f"{nome_cidade} (retorno nulo)")
                
        except FileNotFoundError as e:
            logger.warning(f"     ❌ Arquivo não encontrado: {str(e)[:50]}")
            falhas.append(f"{nome_cidade} (arquivo não encontrado)")
        except Exception as e:
            logger.warning(f"     ❌ Erro: {str(e)[:60]}")
            falhas.append(f"{nome_cidade} ({str(e)[:40]})")
    
    logger.info("\n" + "=" * 60)
    logger.info(f"\n📊 RESULTADO FINAL:")
    logger.info(f"   ✅ Sucesso: {sucesso}/{total}")
    logger.info(f"   ❌ Falhas: {len(falhas)}/{total}")
    
    if falhas:
        logger.info(f"\n❌ Cidades com falha:")
        for falha in falhas[:10]:
            logger.info(f"   - {falha}")
        if len(falhas) > 10:
            logger.info(f"   ... e mais {len(falhas) - 10}")
    
    logger.info(f"\n✨ Taxa de sucesso: {sucesso*100//total}%")
    logger.info("🎉 GERAÇÃO COMPLETA!")

if __name__ == '__main__':
    main()
