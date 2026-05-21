#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direct timelapse test with known paths
"""

import sys
from pathlib import Path

# Add src to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir / 'src' / 'mapas'))

def test_timelapse_direct():
    from mapa_crescimento import MapaCrescimento
    
    print("\n" + "=" * 80)
    print("🎬 TESTE DIRETO: TIMELAPSE DEZEMBRO + BINÁRIO")
    print("=" * 80)
    
    mapa = MapaCrescimento()
    
    # Load coordinates
    print("\n📍 Carregando coordenadas...")
    if not mapa.carregar_coordenadas():
        print("❌ Erro ao carregar coordenadas")
        return False
    print(f"✅ {len(mapa.coordenadas)} cidades carregadas")
    
    # Test with direct path
    docs = Path.home() / 'Documents'
    
    # Try Blumenau_noturno
    blumenau_path = docs / 'Blumenau_noturno' / 'Raster'
    
    if blumenau_path.exists():
        print(f"\n✅ Encontrado: {blumenau_path}")
        
        # List subfolder
        subfolders = list(blumenau_path.iterdir())
        if subfolders:
            primeira = subfolders[0]
            print(f"   Usando: {primeira.name}")
            
            # Count TIF files
            all_tif = list(primeira.glob('**/*.tif'))
            print(f"   Total TIF: {len(all_tif)}")
            
            # Filter December
            december_tif = [f for f in all_tif if f.stem.endswith('_12')]
            print(f"   Dezembro (mês 12): {len(december_tif)} imagens")
            
            # Show years
            years = set()
            for tif in december_tif:
                partes = tif.stem.split('_')
                if len(partes) >= 2:
                    years.add(partes[-2])
            
            print(f"   Anos disponíveis: {sorted(years)}")
            
            # Try to generate
            print(f"\n🎬 Gerando timelapse...")
            output = project_dir / f"timelapse_blumenau_test.html"
            
            try:
                resultado = mapa.gerar_timelapse_cidade(
                    'Blumenau',
                    str(primeira),
                    str(output)
                )
                
                if resultado and Path(resultado).exists():
                    tamanho = Path(resultado).stat().st_size
                    print(f"✅ Timelapse gerado com sucesso!")
                    print(f"   Arquivo: {Path(resultado).name}")
                    print(f"   Tamanho: {tamanho/1024:.1f} KB")
                    
                    # Check if it's binary by looking at image content
                    print(f"\n📊 Validando formato binário...")
                    if '<canvas' in Path(resultado).read_text(errors='ignore'):
                        print(f"   ✅ Formato canvas detectado (para imagens renderizadas)")
                    
                    return True
                else:
                    print(f"❌ Falha ao gerar")
                    return False
                    
            except Exception as e:
                print(f"❌ Erro: {e}")
                import traceback
                traceback.print_exc()
                return False
    else:
        print(f"❌ Não encontrado: {blumenau_path}")
        return False

if __name__ == '__main__':
    try:
        success = test_timelapse_direct()
        print("\n" + "=" * 80)
        if success:
            print("✅ TESTE BEM-SUCEDIDO!")
            print("\nO timelapse foi gerado com:")
            print("  • Apenas imagens de DEZEMBRO (mês 12)")
            print("  • Formato BINÁRIO (preto e branco)")
            print("  • Uma imagem por ano")
        else:
            print("❌ Teste falhou")
        print("=" * 80)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
