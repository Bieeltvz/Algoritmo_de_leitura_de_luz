#!/usr/bin/env python3
"""
Debug: Verificar se coordenadas são carregadas corretamente
"""

from mapa_crescimento import MapaCrescimento
import json

mapa = MapaCrescimento()

print("Carregando coordenadas...")
sucesso = mapa.carregar_coordenadas()
print(f"Resultado: {sucesso}")
print(f"Total de cidades carregadas: {len(mapa.coordenadas)}")

# Procurar por braco
braco_keys = [k for k in mapa.coordenadas.keys() if 'braco' in k.lower()]
print(f"\nChaves com 'braco': {braco_keys}")

if braco_keys:
    for k in braco_keys:
        print(f"  {k}: {mapa.coordenadas[k]}")

# Tentar o exato
if 'braco do trombudo' in mapa.coordenadas:
    print(f"\n✅ 'braco do trombudo' encontrado!")
    print(f"   Coordenadas: {mapa.coordenadas['braco do trombudo']}")
else:
    print(f"\n❌ 'braco do trombudo' NÃO encontrado!")
    
    # Mostrar primeiras 10 chaves
    print(f"\nPrimeiras 10 chaves no dicionário:")
    for i, k in enumerate(list(mapa.coordenadas.keys())[:10]):
        print(f"  {i+1}. {k}")
