import numpy as np
from PIL import Image
import sys
sys.path.insert(0, ".")

# Simular imagem e mapa de crescimento
imagem_cinza = np.random.randint(50, 200, (300, 300), dtype=np.uint8)

# Criar mapa de crescimento sintético
mapa_crescimento = np.zeros((300, 300), dtype=np.uint8)
mapa_crescimento[50:100, 50:100] = 1   # Amarelo
mapa_crescimento[150:200, 150:200] = 2  # Vermelho

# Aplicar overlay
from mapa_crescimento import MapaCrescimento
m = MapaCrescimento()
resultado = m._aplicar_overlay_crescimento(imagem_cinza, mapa_crescimento)

print(f"Tipo resultado: {type(resultado)}, dtype: {resultado.dtype}, shape: {resultado.shape}")
print(f"Cor em amarelo [75, 75]: {resultado[75, 75]}")
print(f"Cor em vermelho [175, 175]: {resultado[175, 175]}")
print(f"Cor em fundo [25, 25]: {resultado[25, 25]}")

# Salvar teste
img_pil = Image.fromarray(resultado, mode='RGB')
img_pil.save('test_overlay_demo.png')
print('OK')
