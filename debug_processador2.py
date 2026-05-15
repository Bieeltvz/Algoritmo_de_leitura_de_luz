"""
Debug direto do processador - simula exatamente o que ele faz
"""

import numpy as np
import rasterio
from pathlib import Path

docs = Path(r"C:\Users\gtvargas\Documents")
tiff_files = list(docs.glob("**/Canelinha*/**/*.tif"))[:1]

if not tiff_files:
    print("Nenhum arquivo")
    exit(1)

tiff = tiff_files[0]
print(f"Arquivo: {tiff.name}\n")

with rasterio.open(tiff) as src:
    dados = src.read(1).astype(float)
    
    mascara_nodata_original = dados == -9999
    mascara_valida = (dados > 0) & (~mascara_nodata_original)
    pixels_validos = dados[mascara_valida]
    
    # DEBUG: Reproducir la lógica exacta del processador
    media_bruta = float(np.mean(pixels_validos))
    mediana_bruta = float(np.median(pixels_validos))
    desvio_bruto = float(np.std(pixels_validos))
    
    max_valor = float(np.max(pixels_validos))
    percentis_baixos = np.percentile(pixels_validos, 50)  # Mediana
    
    print(f"max_valor: {max_valor}")
    print(f"percentis_baixos (mediana): {percentis_baixos}")
    print(f"media_bruta: {media_bruta}")
    print()
    
    print(f"Condição 1: percentis_baixos < 10 and max_valor > 100")
    print(f"  {percentis_baixos} < 10: {percentis_baixos < 10}")
    print(f"  {max_valor} > 100: {max_valor > 100}")
    print(f"  Resultado: {percentis_baixos < 10 and max_valor > 100}")
    print()
    
    print(f"Condição 2: max_valor <= 1.0")
    print(f"  {max_valor} <= 1.0: {max_valor <= 1.0}")
    print()
    
    # Quale condição vai disparar?
    if percentis_baixos < 10 and max_valor > 100:
        media = media_bruta * 255
        print(f"✓ CONVERSÃO 1 aplicada (dados misto)")
        print(f"  {media_bruta:.4f} × 255 = {media:.2f}")
    elif max_valor <= 1.0:
        media = media_bruta * 255
        print(f"✓ CONVERSÃO 2 aplicada (escala 0-1)")
        print(f"  {media_bruta:.4f} × 255 = {media:.2f}")
    else:
        media = media_bruta
        print(f"✗ SEM CONVERSÃO")
        print(f"  Mantém: {media:.2f}")
