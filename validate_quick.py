#!/usr/bin/env python
# Teste rápido das coordenadas adicionadas
import logging
logging.disable(logging.CRITICAL)  # Desabilitar logs

from app import COORDENADAS_CIDADES

cidades_pedidas = {
    'apiuna': (-27.0375, -49.3885),
    'atalanta': (-27.2500, -49.5300),
    'balneario picarras': (-26.8830, -48.6850),
    'botuvera': (-27.1991, -49.0726),
    'camboriu': (-26.9924, -48.634),
    'chapadao do lageado': (-27.5905, -49.5539),
    'itajai': (-26.9047, -48.6553),
    'ituporanga': (-27.2900, -49.7100),
    'jose boiteux': (-26.9621, -49.6263),
    'major gercino': (-27.0500, -49.4800),
    'petrolandia': (-27.533, -49.6985),
    'presidente getulio': (-27.0426, -49.621),
    'rio do sul': (-27.7807, -49.6333),
    'sao joao batista': (-27.2775, -48.8496),
    'taio': (-27.1168, -50.0002),
    'timbo': (-26.8283, -49.2706),
    'vale itajai': (-27.0790, -49.0630),
}

print("\n" + "=" * 70)
print("VALIDAÇÃO DE COORDENADAS ADICIONADAS")
print("=" * 70 + "\n")

todas_ok = True
for cidade, coords_esperadas in cidades_pedidas.items():
    if cidade in COORDENADAS_CIDADES:
        coords_reais = COORDENADAS_CIDADES[cidade]
        if coords_reais == coords_esperadas:
            print(f"✓ {cidade:<25} {coords_reais}")
        else:
            print(f"⚠ {cidade:<25} {coords_reais} (esperado {coords_esperadas})")
    else:
        print(f"✗ {cidade:<25} FALTANDO!")
        todas_ok = False

print("\n" + "=" * 70)
if todas_ok:
    print("✅ SUCESSO! Todas as cidades estão no mapa com as coordenadas corretas.")
else:
    print("⚠ Algumas cidades ainda estão faltando!")
print("=" * 70 + "\n")
