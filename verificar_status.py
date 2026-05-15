#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica o status do processamento de cidades
"""

from pathlib import Path
import sys

DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
sys.path.insert(0, str(DIRETORIO_TRABALHO))

from app import descobrir_pastas_cidades

pastas = descobrir_pastas_cidades()

print("\n" + "=" * 100)
print("STATUS DO PROCESSAMENTO - TODAS AS CIDADES")
print("=" * 100)

cidades_com = []
cidades_sem = []

for chave, info in sorted(pastas.items()):
    arquivo_resultado = DIRETORIO_TRABALHO / f'resultados_{info["nome"]}.csv'
    nome_amigavel = info['nome_amigavel']
    
    if arquivo_resultado.exists():
        linhas = sum(1 for _ in open(arquivo_resultado)) - 1
        cidades_com.append((nome_amigavel, linhas))
    else:
        cidades_sem.append(nome_amigavel)

print(f"\nCIDADES COM RESULTADOS: {len(cidades_com)}/{len(pastas)}")
print("-" * 100)
for nome, linhas in sorted(cidades_com):
    print(f"   OK  {nome}: {linhas} registros")

if cidades_sem:
    print(f"\nCIDADES SEM RESULTADOS: {len(cidades_sem)}/{len(pastas)}")
    print("-" * 100)
    for nome in sorted(cidades_sem):
        print(f"   FALTA  {nome}")

print("\n" + "=" * 100)
print(f"TOTAL: {len(cidades_com)} de {len(pastas)} cidades com dados")
print("=" * 100 + "\n")
