"""
Teste isolado: Processa 1 arquivo com a lógica corrigida
"""

import numpy as np
import rasterio
from pathlib import Path

def processar_arquivo_teste(caminho_arquivo):
    """Simula o processamento com a lógica corrigida"""
    
    caminho_arquivo = Path(caminho_arquivo)
    
    with rasterio.open(caminho_arquivo) as src:
        dados = src.read(1).astype(float)
    
    mascara_nodata_original = dados == -9999
    mascara_valida = (dados > 0) & (~mascara_nodata_original)
    pixels_validos = dados[mascara_valida]
    
    # LÓGICA CORRIGIDA
    media_bruta = float(np.mean(pixels_validos))
    mediana_bruta = float(np.median(pixels_validos))
    desvio_bruto = float(np.std(pixels_validos))
    
    max_valor = float(np.max(pixels_validos))
    percentis_baixos = np.percentile(pixels_validos, 50)
    
    print(f"Arquivo: {caminho_arquivo.name}")
    print(f"Max: {max_valor}, Mediana: {percentis_baixos}")
    
    # Detectar escala
    if percentis_baixos < 10 and max_valor > 100:
        media = media_bruta * 255
        mediana = mediana_bruta * 255
        desvio = desvio_bruto * 255
        print(f"✓ Aplicada CONVERSÃO (dados misto)")
    elif max_valor <= 1.0:
        media = media_bruta * 255
        mediana = mediana_bruta * 255
        desvio = desvio_bruto * 255
        print(f"✓ Aplicada CONVERSÃO (escala 0-1)")
    else:
        media = media_bruta
        mediana = mediana_bruta
        desvio = desvio_bruto
        print(f"✗ SEM conversão (escala 0-255)")
    
    return {
        'media_bruta': round(media_bruta, 2),
        'media_convertida': round(media, 2),
        'mediana_convertida': round(mediana, 2),
        'desvio_convertido': round(desvio, 2),
    }

# Testar
docs = Path(r"C:\Users\gtvargas\Documents")
tiff_files = list(docs.glob("**/Canelinha*/**/*.tif"))[:1]

if tiff_files:
    resultado = processar_arquivo_teste(str(tiff_files[0]))
    print("\nResultados:")
    for k, v in resultado.items():
        print(f"  {k}: {v}")
