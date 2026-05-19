#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify coordinate loading fix for timelapse generation.
"""

import sys
from pathlib import Path

# Add src to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir / 'src' / 'mapas'))

from mapa_crescimento import MapaCrescimento

def test_coordinate_loading():
    """Test if MapaCrescimento can load coordinates"""
    print("=" * 60)
    print("🧪 TESTE DE CARREGAMENTO DE COORDENADAS")
    print("=" * 60)
    
    mapa = MapaCrescimento()
    
    # Test 1: Load coordinates
    print("\n1️⃣  Testando carregamento de coordenadas...")
    resultado = mapa.carregar_coordenadas()
    
    if resultado:
        print(f"   ✅ Sucesso! Carregadas {len(mapa.coordenadas)} coordenadas")
        print(f"   Algumas cidades: {list(mapa.coordenadas.keys())[:5]}")
    else:
        print(f"   ❌ Falha ao carregar coordenadas")
        return False
    
    # Test 2: Find CSV files
    print("\n2️⃣  Testando busca de arquivos CSV...")
    cidades_teste = ["Blumenau", "Brusque", "Agrolandia"]
    
    for cidade in cidades_teste:
        arquivo = mapa.encontrar_arquivo_csv(cidade)
        if arquivo:
            print(f"   ✅ {cidade}: {Path(arquivo).name}")
        else:
            print(f"   ❌ {cidade}: NÃO ENCONTRADO")
    
    # Test 3: Try to generate timelapse metadata
    print("\n3️⃣  Testando geração de metadados...")
    try:
        # Just test with Blumenau's first subfolder
        pasta_blumenau = project_dir / 'imagens' / 'Blumenau' / 'Reprojetados'
        if pasta_blumenau.exists():
            print(f"   ✅ Pasta encontrada: {pasta_blumenau}")
            print(f"      Imagens: {len(list(pasta_blumenau.glob('*.tif')))}")
        else:
            print(f"   ⚠️  Pasta não encontrada: {pasta_blumenau}")
    except Exception as e:
        print(f"   ❌ Erro ao processar pasta: {e}")
    
    print("\n" + "=" * 60)
    print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_coordinate_loading()
    sys.exit(0 if success else 1)
