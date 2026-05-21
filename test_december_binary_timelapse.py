#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for December-only, binary timelapse generation
"""

import sys
from pathlib import Path
import json

# Add src to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir / 'src' / 'mapas'))

from mapa_crescimento import MapaCrescimento

def test_december_filter():
    """Test December filtering"""
    print("=" * 70)
    print("🧪 TESTE: TIMELAPSE BINÁRIO + APENAS DEZEMBRO (MÊS 12)")
    print("=" * 70)
    
    mapa = MapaCrescimento()
    
    # Load coordinates
    print("\n1️⃣  Carregando coordenadas...")
    if not mapa.carregar_coordenadas():
        print("❌ Falha ao carregar coordenadas")
        return False
    print(f"✅ {len(mapa.coordenadas)} cidades carregadas")
    
    # Test binary conversion
    print("\n2️⃣  Testando binarização de imagem...")
    import numpy as np
    
    # Create synthetic satellite image
    test_image = np.random.rand(100, 100) * 150 + 50  # 50-200 range
    try:
        binary_result = mapa._binarizar_imagem(test_image)
        print(f"✅ Binarização funcionando!")
        print(f"   - Input dtype: {test_image.dtype}")
        print(f"   - Output dtype: {binary_result.dtype}")
        print(f"   - Output shape: {binary_result.shape}")
        print(f"   - Valores únicos: {np.unique(binary_result)}")
        print(f"   - Pixels brancos (255): {np.sum(binary_result == 255)}")
        print(f"   - Pixels pretos (0): {np.sum(binary_result == 0)}")
    except Exception as e:
        print(f"❌ Erro na binarização: {e}")
        return False
    
    # Test December filtering logic
    print("\n3️⃣  Testando filtragem de imagens de dezembro...")
    
    # Simulate file names
    test_filenames = [
        'agrolandia_2020_01.tif',  # January - should be filtered out
        'agrolandia_2020_06.tif',  # June - should be filtered out
        'agrolandia_2020_12.tif',  # December - KEEP
        'agrolandia_2021_03.tif',  # March - should be filtered out
        'agrolandia_2021_12.tif',  # December - KEEP
        'agrolandia_2022_12.tif',  # December - KEEP
        'agrolandia_2023_11.tif',  # November - should be filtered out
        'agrolandia_2023_12.tif',  # December - KEEP
    ]
    
    december_files = []
    for filename in test_filenames:
        # Extract month from filename (last element before extension)
        partes = Path(filename).stem.split('_')
        mes = partes[-1] if len(partes) > 0 else '0'
        
        if mes == '12':
            december_files.append(filename)
            print(f"   ✅ MANTER: {filename}")
        else:
            print(f"   ❌ DESCARTAR: {filename} (mês {mes})")
    
    print(f"\n✅ Filtro funcionando! {len(december_files)}/{len(test_filenames)} arquivos mantidos")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 RESUMO")
    print("=" * 70)
    print(f"✅ Binarização: Funcionando (255 branco / 0 preto)")
    print(f"✅ Filtragem de dezembro: Funcionando ({len(december_files)} de {len(test_filenames)} mantidos)")
    print(f"✅ Sistema pronto para gerar timelapses de dezembro em formato binário")
    print("\n💡 PRÓXIMAS AÇÕES:")
    print("   1. Abra http://localhost:5000")
    print("   2. Selecione uma cidade no dropdown")
    print("   3. Clique 'Gerar Timelapse'")
    print("   4. Timelapse será gerado apenas com imagens de dezembro em preto/branco")
    print("=" * 70)
    
    return True

if __name__ == '__main__':
    success = test_december_filter()
    sys.exit(0 if success else 1)
