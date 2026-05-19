#!/usr/bin/env python3
"""
Debug direto do problema
"""

import numpy as np
from mapa_crescimento import MapaCrescimento

m = MapaCrescimento()

# Criar dados com crescimento claro
np.random.seed(42)
img2014 = np.random.randint(40, 100, (256, 256)).astype(np.float32)
img2024 = img2014.copy()

# Adicionar crescimento forte em uma área (100x100 = 10000 pixels)
img2024[50:150, 50:150] += 20

print("=== Teste: Dados com crescimento de +20 ===\n")

# Calcular manualmente
diferenca = img2024 - img2014
print(f"Total de pixels: {diferenca.size}")
print(f"Pixels com diferença > 0: {np.sum(diferenca > 0)}")
print(f"Pixels com diferença > 20: {np.sum(diferenca > 20)}")
print(f"Diferença - min: {diferenca.min():.2f}, max: {diferenca.max():.2f}")

# Preparar para cálculo como no código
diff_crescimento = diferenca[~np.isnan(diferenca) & ~np.isinf(diferenca) & (diferenca > 0)]
print(f"\nPixels de crescimento positivo: {len(diff_crescimento)}")

if len(diff_crescimento) > 0:
    mediana = np.median(diff_crescimento)
    p75 = np.percentile(diff_crescimento, 75)
    p95 = np.percentile(diff_crescimento, 95)
    
    print(f"Mediana do crescimento: {mediana:.2f}")
    print(f"P75 do crescimento: {p75:.2f}")
    print(f"P95 do crescimento: {p95:.2f}")
    
    # Contar quantos pixels passariam em cada filtro
    pixels_acima_mediana = np.sum(diferenca > mediana)
    pixels_acima_p75 = np.sum(diferenca > p75)
    pixels_entre = np.sum((diferenca > mediana) & (diferenca <= p75))
    
    print(f"\nPixels com diferença > mediana: {pixels_acima_mediana}")
    print(f"Pixels com diferença > p75: {pixels_acima_p75}")
    print(f"Pixels entre mediana e p75: {pixels_entre}")

# Agora chamar a função
print("\n=== Chamando _calcular_mapa_crescimento ===\n")
mapa = m._calcular_mapa_crescimento(img2014, img2024)

if mapa is not None:
    count_0 = np.sum(mapa == 0)
    count_1 = np.sum(mapa == 1)
    count_2 = np.sum(mapa == 2)
    total = mapa.size
    
    print(f"Resultado do mapa:")
    print(f"  0s (sem mudança): {count_0} ({count_0/total*100:.1f}%)")
    print(f"  1s (amarelo):     {count_1} ({count_1/total*100:.1f}%)")
    print(f"  2s (vermelho):    {count_2} ({count_2/total*100:.1f}%)")
else:
    print("Mapa é None!")
