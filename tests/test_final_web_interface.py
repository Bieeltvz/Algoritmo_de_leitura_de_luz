#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste final: Simulacao da interface web
Braco Do Trombudo - Gerar Timelapse e Mapa
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento
import os
import sys

os.chdir(Path(__file__).parent)

print("=" * 70)
print("TESTE FINAL: INTERFACE WEB BRACO DO TROMBUDO")
print("=" * 70)

mapa = MapaCrescimento()

# Step 1: Carregar coordenadas (como app.py faz no startup)
print("\n[STARTUP] Carregando coordenadas...")
if not mapa.carregar_coordenadas():
    print("ERRO: Nao conseguiu carregar coordenadas!")
    sys.exit(1)
print(f"OK: {len(mapa.coordenadas)} cidades carregadas")

# Step 2: Usuario clica em "Braco Do Trombudo" e seleciona
pasta_selecionada = {
    'nome': 'Braco_Do_Trombudo_recortes',
    'nome_amigavel': 'Braco Do Trombudo - Braco Do Trombudo'
}

print(f"\n[USER] Selecionou: {pasta_selecionada['nome_amigavel']}")

# Step 3: Clica em "Gerar Timelapse"
print(f"\n[ACTION] Clicou em 'Gerar Timelapse'")
print("  (chamando /api/gerar-timelapse)")

arquivo_timelapse = f"timelapse_{pasta_selecionada['nome']}_final.html"
resultado_timelapse = mapa.gerar_timelapse_cidade(pasta_selecionada['nome'], arquivo_timelapse)

if resultado_timelapse and Path(resultado_timelapse).exists():
    tamanho = Path(resultado_timelapse).stat().st_size / 1024 / 1024
    print(f"  ✅ SUCESSO: Timelapse gerado ({tamanho:.1f} MB)")
else:
    print(f"  ❌ ERRO: Falha ao gerar timelapse")
    sys.exit(1)

# Step 4: Clica em "Gerar Mapa Interativo"
print(f"\n[ACTION] Clicou em 'Gerar Mapa Interativo'")
print("  (chamando /api/gerar-mapa-crescimento)")

arquivo_mapa = f"mapa_{pasta_selecionada['nome']}_final.html"
resultado_mapa = mapa.gerar_relatorio_html_cidade(pasta_selecionada['nome'], arquivo_mapa)

if resultado_mapa and Path(resultado_mapa).exists():
    tamanho = Path(resultado_mapa).stat().st_size / 1024
    print(f"  ✅ SUCESSO: Mapa gerado ({tamanho:.1f} KB)")
else:
    print(f"  ❌ ERRO: Falha ao gerar mapa")
    sys.exit(1)

# Summary
print("\n" + "=" * 70)
print("RESULTADO FINAL")
print("=" * 70)
print(f"✅ Timelapse: FUNCIONANDO")
print(f"✅ Mapa: FUNCIONANDO")
print(f"\n✅ PROBLEMA RESOLVIDO!")
print(f"\nOs usuários agora podem gerar tanto timelapse quanto mapa para")
print(f"Braco Do Trombudo sem erros.")
print("=" * 70)
