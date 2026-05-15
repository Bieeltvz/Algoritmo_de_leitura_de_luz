#!/usr/bin/env python3
"""
Teste simples do algoritmo de detecção de crescimento
"""

import numpy as np
from PIL import Image
from mapa_crescimento import MapaCrescimento
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

m = MapaCrescimento()

print("=== Teste 1: Crescimento localizado ===\n")

# Criar imagens base
imagem_inicio = np.ones((512, 512), dtype=np.float32) * 100.0
imagem_fim = imagem_inicio.copy()

# Área com crescimento moderado
imagem_fim[50:150, 50:150] = 110.0

# Área com crescimento forte  
imagem_fim[250:350, 250:350] = 125.0

# Calcular mapa de crescimento
mapa = m._calcular_mapa_crescimento(imagem_inicio, imagem_fim)

if mapa is not None:
    pixels_nada = np.sum(mapa == 0)
    pixels_amarelo = np.sum(mapa == 1)
    pixels_vermelho = np.sum(mapa == 2)
    total = mapa.size
    
    print(f"Pixels sem mudança: {pixels_nada} ({pixels_nada/total*100:.1f}%)")
    print(f"Pixels amarelos:    {pixels_amarelo} ({pixels_amarelo/total*100:.1f}%)")
    print(f"Pixels vermelhos:   {pixels_vermelho} ({pixels_vermelho/total*100:.1f}%)")
    
    # Converter para uint8
    imagem_cinza = (imagem_inicio * 0.8).astype(np.uint8)
    
    # Aplicar overlay
    resultado = m._aplicar_overlay_crescimento(imagem_cinza, mapa)
    img = Image.fromarray(resultado, mode='RGB')
    img = img.resize((900, 900))
    img.save('test_growth_demo.png')
    print("\n✅ Imagem salva: test_growth_demo.png")
