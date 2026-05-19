#!/usr/bin/env python3
"""
Teste detalhado do algoritmo de detecção de crescimento
"""

import numpy as np
from mapa_crescimento import MapaCrescimento
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

m = MapaCrescimento()

# Caso 1: Imagem com crescimento localizado
print("=== TESTE 1: Crescimento localizado ===")
imagem_inicio = np.random.randint(80, 120, (512, 512)).astype(np.float32)
imagem_fim = imagem_inicio.copy()

# Adicionar crescimento em duas áreas
imagem_fim[50:150, 50:150] += np.random.uniform(5, 10, (100, 100))  # Amarelo (moderado)
imagem_fim[250:350, 250:350] += np.random.uniform(15, 25, (100, 100))  # Vermelho (forte)

mapa = m._calcular_mapa_crescimento(imagem_inicio, imagem_fim)

if mapa is not None:
    total = mapa.shape[0] * mapa.shape[1]
    pixels_amarelo = np.sum(mapa == 1)
    pixels_vermelho = np.sum(mapa == 2)
    pixels_nada = np.sum(mapa == 0)
    
    print(f"Total de pixels: {total}")
    print(f"Pixels sem mudança: {pixels_nada} ({pixels_nada/total*100:.1f}%)")
    print(f"Pixels amarelos (moderado): {pixels_amarelo} ({pixels_amarelo/total*100:.1f}%)")
    print(f"Pixels vermelhos (forte): {pixels_vermelho} ({pixels_vermelho/total*100:.1f}%)")
    
    # Visualizar
    from PIL import Image
    resultado = m._aplicar_overlay_crescimento((imagem_inicio.astype(np.uint8) ), mapa)
    img = Image.fromarray(resultado, mode='RGB')
    img.save('test_growth_localized.png')
    print("✅ Imagem salva: test_growth_localized.png\n")

# Caso 2: Imagem sem crescimento
print("=== TESTE 2: Sem crescimento ===")
imagem_inicio2 = np.random.randint(100, 130, (512, 512), dtype=np.float32)
imagem_fim2 = imagem_inicio2 + np.random.uniform(-2, 2, (512, 512))  # Ruído pequeno

mapa2 = m._calcular_mapa_crescimento(imagem_inicio2, imagem_fim2)

if mapa2 is not None:
    total2 = mapa2.shape[0] * mapa2.shape[1]
    pixels_amarelo2 = np.sum(mapa2 == 1)
    pixels_vermelho2 = np.sum(mapa2 == 2)
    pixels_nada2 = np.sum(mapa2 == 0)
    
    print(f"Total de pixels: {total2}")
    print(f"Pixels sem mudança: {pixels_nada2} ({pixels_nada2/total2*100:.1f}%)")
    print(f"Pixels amarelos (moderado): {pixels_amarelo2} ({pixels_amarelo2/total2*100:.1f}%)")
    print(f"Pixels vermelhos (forte): {pixels_vermelho2} ({pixels_vermelho2/total2*100:.1f}%)")
    
    resultado2 = m._aplicar_overlay_crescimento((imagem_inicio2.astype(np.uint8) ), mapa2)
    img2 = Image.fromarray(resultado2, mode='RGB')
    img2.save('test_growth_none.png')
    print("✅ Imagem salva: test_growth_none.png\n")

# Caso 3: Crescimento uniforme
print("=== TESTE 3: Crescimento uniforme em toda a imagem ===")
imagem_inicio3 = np.full((512, 512), 100, dtype=np.float32)
imagem_fim3 = np.full((512, 512), 120, dtype=np.float32)  # Crescimento uniforme de 20

mapa3 = m._calcular_mapa_crescimento(imagem_inicio3, imagem_fim3)

if mapa3 is not None:
    total3 = mapa3.shape[0] * mapa3.shape[1]
    pixels_amarelo3 = np.sum(mapa3 == 1)
    pixels_vermelho3 = np.sum(mapa3 == 2)
    pixels_nada3 = np.sum(mapa3 == 0)
    
    print(f"Total de pixels: {total3}")
    print(f"Pixels sem mudança: {pixels_nada3} ({pixels_nada3/total3*100:.1f}%)")
    print(f"Pixels amarelos (moderado): {pixels_amarelo3} ({pixels_amarelo3/total3*100:.1f}%)")
    print(f"Pixels vermelhos (forte): {pixels_vermelho3} ({pixels_vermelho3/total3*100:.1f}%)")
    
    resultado3 = m._aplicar_overlay_crescimento((imagem_inicio3.astype(np.uint8) ), mapa3)
    img3 = Image.fromarray(resultado3, mode='RGB')
    img3.save('test_growth_uniform.png')
    print("✅ Imagem salva: test_growth_uniform.png\n")

print("✅ Testes concluídos!")
