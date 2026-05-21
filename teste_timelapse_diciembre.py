#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test real timelapse generation with December filter + binary
"""

import sys
from pathlib import Path
import json

# Add src to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir / 'src' / 'mapas'))

def test_real_timelapse():
    """Test actual timelapse generation"""
    from mapa_crescimento import MapaCrescimento
    
    print("\n" + "=" * 80)
    print("🎬 TESTE REAL: GERAÇÃO DE TIMELAPSE COM DEZEMBRO + BINÁRIO")
    print("=" * 80)
    
    mapa = MapaCrescimento()
    
    # Load coordinates
    print("\n📍 Carregando coordenadas...")
    if not mapa.carregar_coordenadas():
        print("❌ Falha ao carregar coordenadas")
        return False
    print(f"✅ {len(mapa.coordenadas)} cidades carregadas")
    
    # Test with Blumenau city (which has multiple data folders)
    teste_cidades = ['Blumenau', 'Brusque', 'Bombinhas']
    
    for cidade in teste_cidades:
        print(f"\n{'='*80}")
        print(f"🏙️  Testando cidade: {cidade}")
        print(f"{'='*80}")
        
        try:
            # Try to find the city path
            from pathlib import Path
            import os
            
            # Look for city folder in Documents
            docs_path = Path.home() / 'Documents'
            
            cidade_pattern = cidade.replace(' ', '_').lower()
            cidade_patterns = [
                f"{cidade}_noturno",
                f"{cidade}",
                cidade.replace(' ', '_'),
            ]
            
            found_paths = []
            
            if docs_path.exists():
                for item in docs_path.iterdir():
                    if item.is_dir():
                        item_lower = item.name.lower()
                        for pattern in cidade_patterns:
                            if pattern in item_lower:
                                found_paths.append(item)
                                break
            
            if not found_paths:
                print(f"   ⚠️  Não encontrei pasta para {cidade}")
                continue
            
            print(f"   📁 Pastas encontradas: {len(found_paths)}")
            
            for pasta in found_paths[:1]:  # Test with first folder
                raster_path = pasta / 'Raster'
                
                if raster_path.exists():
                    print(f"   📂 Analisando: {raster_path.name}")
                    
                    # List all recortes/folders
                    recortes = [d for d in raster_path.iterdir() if d.is_dir()]
                    
                    if recortes:
                        primeira_recorte = recortes[0]
                        print(f"   🖼️  Recorte: {primeira_recorte.name}")
                        
                        # Count TIF files by month
                        todos_tif = list(primeira_recorte.glob('**/*.tif'))
                        print(f"   📊 Total de TIFs: {len(todos_tif)}")
                        
                        # Count by month
                        meses_count = {}
                        for tif in todos_tif:
                            partes = tif.stem.split('_')
                            if len(partes) > 0:
                                mes = partes[-1]
                                meses_count[mes] = meses_count.get(mes, 0) + 1
                        
                        print(f"   📅 Distribuição por mês:")
                        for mes in sorted(meses_count.keys()):
                            count = meses_count[mes]
                            marker = "✅ DEZEMBRO" if mes == "12" else "  "
                            print(f"       Mês {mes}: {count:3d} imagens  {marker}")
                        
                        # Now try to generate timelapse
                        print(f"\n   🎬 Tentando gerar timelapse...")
                        output_file = project_dir / f"timelapse_teste_{cidade}_{primeira_recorte.name}.html"
                        
                        resultado = mapa.gerar_timelapse_cidade(
                            cidade, 
                            str(primeira_recorte), 
                            str(output_file)
                        )
                        
                        if resultado and Path(resultado).exists():
                            tamanho_kb = Path(resultado).stat().st_size / 1024
                            print(f"   ✅ Timelapse gerado: {Path(resultado).name}")
                            print(f"   📦 Tamanho: {tamanho_kb:.1f} KB")
                        else:
                            print(f"   ❌ Falha ao gerar timelapse")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    print("\n" + "=" * 80)
    print("✅ TESTE COMPLETO")
    print("=" * 80)
    return True

if __name__ == '__main__':
    try:
        success = test_real_timelapse()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
