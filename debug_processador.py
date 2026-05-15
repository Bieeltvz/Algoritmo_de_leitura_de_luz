"""
Debug: Verifica os valores reais dentro do processador
"""

import numpy as np
import rasterio
from pathlib import Path

# Pegar um arquivo de exemplo
docs = Path(r"C:\Users\gtvargas\Documents")
tiff_files = list(docs.glob("**/Canelinha*/**/*.tif"))[:1]

if not tiff_files:
    print("Nenhum arquivo encontrado")
    exit(1)

tiff = tiff_files[0]
print(f"Analisando: {tiff.name}\n")

with rasterio.open(tiff) as src:
    dados = src.read(1).astype(float)
    
    # Reproduzir exatamente o que o processador faz
    mascara_nodata_original = dados == -9999
    mascara_valida = (dados > 0) & (~mascara_nodata_original)
    pixels_validos = dados[mascara_valida]
    
    print(f"Dados brutos (primeiros 20):")
    print(pixels_validos[:20])
    print()
    
    print(f"Estatísticas dos dados brutos:")
    print(f"  - Max: {np.max(pixels_validos):.6f}")
    print(f"  - Mean: {np.mean(pixels_validos):.6f}")
    print(f"  - Min: {np.min(pixels_validos):.6f}")
    print()
    
    # Checar se a conversão deveria acontecer
    max_valor = float(np.max(pixels_validos))
    print(f"Max valor: {max_valor}")
    print(f"Max <= 1.0? {max_valor <= 1.0}")
    
    if max_valor <= 1.0:
        media_convertida = np.mean(pixels_validos) * 255
        print(f"\n✓ Conversão será aplicada!")
        print(f"  Média × 255 = {media_convertida:.2f}")
    else:
        print(f"\n✗ Conversão NÃO será aplicada")
        print(f"  Dados estão em escala > 1.0")
