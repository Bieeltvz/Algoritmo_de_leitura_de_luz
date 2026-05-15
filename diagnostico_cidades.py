#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para investigar problemas com descoberta de cidades
"""

from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

CAMINHO_DOCUMENTOS = Path(r"C:\Users\gtvargas\Documents")

print("=" * 100)
print("DIAGNÓSTICO: INVESTIGANDO CIDADES NÃO DESCOBERTAS")
print("=" * 100)

# Verificar se Documentos existe
print(f"\n[1] Verificando CAMINHO_DOCUMENTOS: {CAMINHO_DOCUMENTOS}")
print(f"    Existe: {CAMINHO_DOCUMENTOS.exists()}")

# Procurar especificamente por balneario_camboriu e balneario_picarras
print("\n[2] Procurando especificamente por Balneário Camboriú e Balneário Picarras...")

cidades_procurar = [
    "balneario_camboriu_noturno",
    "Balneario_Picarras_noturno"
]

for cidade_nome in cidades_procurar:
    cidade_dir = CAMINHO_DOCUMENTOS / cidade_nome
    print(f"\n  Procurando: {cidade_nome}")
    print(f"    Caminho completo: {cidade_dir}")
    print(f"    Existe: {cidade_dir.exists()}")
    
    if not cidade_dir.exists():
        # Tentar encontrar similar (case-insensitive)
        print(f"    Procurando alternativas (case-insensitive)...")
        for item in CAMINHO_DOCUMENTOS.iterdir():
            if item.is_dir() and item.name.lower() == cidade_nome.lower():
                print(f"      ✓ Encontrado com nome diferente: {item.name}")
                cidade_dir = item
                break
    
    if cidade_dir.exists():
        print(f"    ✓ Diretório encontrado!")
        
        # Procurar por Raster
        print(f"    Procurando pasta Raster...")
        raster_dir = None
        for item in cidade_dir.iterdir():
            print(f"      - {item.name} (dir: {item.is_dir()})")
            if item.is_dir() and item.name.lower() == 'raster':
                raster_dir = item
                print(f"        ✓ Encontrada pasta Raster: {item.name}")
        
        if raster_dir:
            print(f"    Procurando pastas de recorte dentro de Raster...")
            for recorte_dir in raster_dir.iterdir():
                if recorte_dir.is_dir():
                    # Contar imagens
                    tif_files = list(recorte_dir.glob('*/*.tif')) + list(recorte_dir.glob('*.tif'))
                    print(f"      - {recorte_dir.name} ({len(tif_files)} imagens TIF)")
                    
                    # Listar alguns arquivos
                    if tif_files:
                        for tif in tif_files[:3]:
                            print(f"        * {tif.name}")
                        if len(tif_files) > 3:
                            print(f"        ... e mais {len(tif_files) - 3} arquivos")
        else:
            print(f"    ✗ Pasta Raster NÃO encontrada!")
            print(f"    Conteúdo do diretório:")
            for item in cidade_dir.iterdir():
                print(f"      - {item.name} (dir: {item.is_dir()})")

print("\n" + "=" * 100)
print("DIAGNÓSTICO CONCLUÍDO")
print("=" * 100)
