#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE FINAL SIMPLIFICADO
Verificação rápida que o mapa de Braco Do Trombudo funciona
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento
import os

os.chdir(Path(__file__).parent)

print("=" * 70)
print("TESTE: Map Generation - Braco Do Trombudo")
print("=" * 70)

mapa = MapaCrescimento()
mapa.carregar_coordenadas()

nome_cidade = "Braco_Do_Trombudo_recortes"

# Test 1: Calcular crescimento (que alimenta o mapa)
print(f"\n[1] Calcular crescimento...")
dados = mapa.calcular_crescimento_cidade_unica(nome_cidade)

if dados and dados.get('crescimento') is not None:
    print(f"    ✅ Dados: {dados}")
    print(f"       - Crescimento: {dados['crescimento']}%")
    print(f"       - Lat: {dados['lat']}, Lon: {dados['lon']}")
else:
    print(f"    ❌ Falha: {dados}")
    exit(1)

# Test 2: Gerar mapa
print(f"\n[2] Gerando mapa HTML...")
arquivo_mapa = f'test_mapa_{nome_cidade}.html'
resultado = mapa.gerar_relatorio_html_cidade(nome_cidade, arquivo_mapa)

if resultado and Path(resultado).exists():
    tamanho = Path(resultado).stat().st_size / 1024
    print(f"    ✅ Mapa gerado com sucesso!")
    print(f"       - Arquivo: {resultado}")
    print(f"       - Tamanho: {tamanho:.1f} KB")
else:
    print(f"    ❌ Falha na geração do mapa")
    exit(1)

# Summary
print("\n" + "=" * 70)
print("✅ PROBLEMA RESOLVIDO!")
print("=" * 70)
print("Braco Do Trombudo agora funciona:")
print("  ✅ Crescimento calculado corretamente")
print("  ✅ Mapa interativo gerado com sucesso")
print("=" * 70)
