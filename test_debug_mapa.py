#!/usr/bin/env python3
"""
Debug: Ver o que _calcular_mapa_crescimento está produzindo
"""

import numpy as np
from PIL import Image
from mapa_crescimento import MapaCrescimento
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

m = MapaCrescimento()

# Teste 1: Dados completamente sem mudança
print("=== Teste 1: Dados sem mudança ===\n")
imagem_cinza = np.ones((256, 256), dtype=np.float32) * 100.0
mapa = m._calcular_mapa_crescimento(imagem_cinza, imagem_cinza)

if mapa is not None:
    print(f"Mapa - 0s: {np.sum(mapa == 0)}, 1s: {np.sum(mapa == 1)}, 2s: {np.sum(mapa == 2)}")

# Teste 2: Dados com ruído pequeno
print("\n=== Teste 2: Com ruído pequeno (-0.5 a +0.5) ===\n")
img1 = np.ones((256, 256), dtype=np.float32) * 100.0
img2 = img1 + np.random.uniform(-0.5, 0.5, (256, 256))
mapa = m._calcular_mapa_crescimento(img1, img2)

if mapa is not None:
    print(f"Mapa - 0s: {np.sum(mapa == 0)}, 1s: {np.sum(mapa == 1)}, 2s: {np.sum(mapa == 2)}")

# Teste 3: Dados com ruído moderado
print("\n=== Teste 3: Com ruído moderado (-2 a +2) ===\n")
img1 = np.ones((256, 256), dtype=np.float32) * 100.0
img2 = img1 + np.random.uniform(-2, 2, (256, 256))
mapa = m._calcular_mapa_crescimento(img1, img2)

if mapa is not None:
    print(f"Mapa - 0s: {np.sum(mapa == 0)}, 1s: {np.sum(mapa == 1)}, 2s: {np.sum(mapa == 2)}")

# Teste 4: Dados muito similares a 2024
print("\n=== Teste 4: Dados realistas com crescimento localizado ===\n")
np.random.seed(42)
img2014 = np.random.randint(40, 100, (256, 256)).astype(np.float32)
img2024 = img2014.copy()

# Adicionar muito crescimento em uma área
img2024[50:150, 50:150] += 20

diferenca = img2024 - img2014
print(f"Diferença: min={diferenca.min():.2f}, max={diferenca.max():.2f}, mean={diferenca.mean():.2f}")
print(f"Pixels com diferença > 0: {np.sum(diferenca > 0)}")

mapa = m._calcular_mapa_crescimento(img2014, img2024)

if mapa is not None:
    total = mapa.size
    count_0 = np.sum(mapa == 0)
    count_1 = np.sum(mapa == 1)
    count_2 = np.sum(mapa == 2)
    print(f"\nMapa - 0s: {count_0} ({count_0/total*100:.1f}%)")
    print(f"        1s: {count_1} ({count_1/total*100:.1f}%)")  
    print(f"        2s: {count_2} ({count_2/total*100:.1f}%)")
