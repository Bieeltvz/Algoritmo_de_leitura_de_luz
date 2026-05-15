#!/usr/bin/env python3
"""
Teste de detecção de crescimento com crescimento forte
"""

import numpy as np
from PIL import Image
from mapa_crescimento import MapaCrescimento
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

m = MapaCrescimento()

print("=== Teste: Crescimento forte ===\n")

# Criar imagens com crescimento mais realista
imagem_inicio = np.ones((512, 512), dtype=np.float32) * 50.0
imagem_fim = imagem_inicio.copy()

# Área sem mudança
imagem_fim[0:100, 0:100] = 50.0

# Área com crescimento moderado (diferença ~5-10)
imagem_fim[100:250, 100:250] = 57.0

# Área com crescimento forte (diferença ~15-20)
imagem_fim[250:400, 250:400] = 67.0

# Calcular diferença para debug
diferenca = imagem_fim - imagem_inicio

print(f"Diferença min: {diferenca.min():.2f}")
print(f"Diferença max: {diferenca.max():.2f}")
print(f"Diferença média: {diferenca.mean():.2f}")

# Apenas valores positivos
diff_positivos = diferenca[diferenca > 0]
if len(diff_positivos) > 0:
    print(f"Diferença positiva min: {diff_positivos.min():.2f}")
    print(f"Diferença positiva max: {diff_positivos.max():.2f}")
    print(f"Mediana: {np.median(diff_positivos):.2f}")
    print(f"P75: {np.percentile(diff_positivos, 75):.2f}")
    print(f"P90: {np.percentile(diff_positivos, 90):.2f}")

print()

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
    imagem_cinza = np.clip(imagem_inicio * 2.5, 0, 255).astype(np.uint8)
    
    # Aplicar overlay
    resultado = m._aplicar_overlay_crescimento(imagem_cinza, mapa)
    img = Image.fromarray(resultado, mode='RGB')
    img = img.resize((900, 900))
    img.save('test_growth_strong.png')
    print("\n✅ Imagem salva: test_growth_strong.png")
