#!/usr/bin/env python3
"""
Teste simulando dados reais com diferenças muito pequenas (como acontece em 2014-2024)
"""

import numpy as np
from PIL import Image
from mapa_crescimento import MapaCrescimento
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

m = MapaCrescimento()

print("=== Teste: Dados reais com pequenas diferenças ===\n")

# Simular dados reais: 2014 vs 2024
# Valores são valores reais de pixels de satélite (tipicamente 0-255 para imagens normalizadas)
np.random.seed(42)
imagem_2014 = np.random.randint(30, 80, (512, 512)).astype(np.float32)
imagem_2024 = imagem_2014.copy()

# Adicionar pequenas variações (ruído) 
imagem_2024 += np.random.normal(0, 1.5, (512, 512))

# Área com crescimento real (pequeno)
imagem_2024[100:200, 100:200] += np.random.normal(0.8, 0.3, (100, 100))

# Área com crescimento moderado
imagem_2024[250:350, 250:350] += np.random.normal(2.5, 0.5, (100, 100))

# Calcular diferença para debug
diferenca = imagem_2024 - imagem_2014
diff_positivos = diferenca[diferenca > 0]

print(f"Diferença geral - min: {diferenca.min():.3f}, max: {diferenca.max():.3f}, média: {diferenca.mean():.3f}")
print(f"Diferença positiva - count: {len(diff_positivos)}, min: {diff_positivos.min():.3f}, max: {diff_positivos.max():.3f}")
if len(diff_positivos) > 0:
    print(f"  mediana: {np.median(diff_positivos):.3f}")
    print(f"  p50: {np.percentile(diff_positivos, 50):.3f}")
    print(f"  p75: {np.percentile(diff_positivos, 75):.3f}")
    print(f"  p90: {np.percentile(diff_positivos, 90):.3f}")
    print(f"  p95: {np.percentile(diff_positivos, 95):.3f}")
    print(f"  p99: {np.percentile(diff_positivos, 99):.3f}")

print()

# Calcular mapa de crescimento
mapa = m._calcular_mapa_crescimento(imagem_2014, imagem_2024)

if mapa is not None:
    pixels_nada = np.sum(mapa == 0)
    pixels_amarelo = np.sum(mapa == 1)
    pixels_vermelho = np.sum(mapa == 2)
    total = mapa.size
    
    print(f"Resultado do mapa de crescimento:")
    print(f"  Sem mudança: {pixels_nada} ({pixels_nada/total*100:.1f}%)")
    print(f"  Amarelos:    {pixels_amarelo} ({pixels_amarelo/total*100:.1f}%)")
    print(f"  Vermelhos:   {pixels_vermelho} ({pixels_vermelho/total*100:.1f}%)")
    
    # Converter para uint8
    imagem_cinza = np.clip(imagem_2014, 0, 255).astype(np.uint8)
    
    # Aplicar overlay
    resultado = m._aplicar_overlay_crescimento(imagem_cinza, mapa)
    img = Image.fromarray(resultado, mode='RGB')
    img = img.resize((900, 900))
    img.save('test_growth_realistic.png')
    print("\n✅ Imagem salva: test_growth_realistic.png")
