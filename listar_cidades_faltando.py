#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para mostrar quais cidades faltam arquivo
"""

from pathlib import Path
import sys

DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
sys.path.insert(0, str(DIRETORIO_TRABALHO))

from app import descobrir_pastas_cidades

# Cidades com arquivo
cidades_com_arquivo = {
    'Agrolandia_recortes',
    'Agronomica_noturna', 
    'Apiuna_recorte',
    'Ascurra_recorte',
    'Aurora_recortes',
    'Barra_Velha_Noturna',
    'BNU_RECORTADO',
    'Braco_Do_Trombudo_recortes',
    'Canelinha_recortes',
    'padrao',
    'picarras_recortado'
}

pastas = descobrir_pastas_cidades()

print("=" * 100)
print("CIDADES COM ARQUIVO: {}".format(len(cidades_com_arquivo)))
print("=" * 100)
for nome in sorted(cidades_com_arquivo):
    print("  OK: resultados_{}.csv".format(nome))

print("\n" + "=" * 100)
print("CIDADES SEM ARQUIVO: {} (de {} descobertas)".format(len(pastas) - len(cidades_com_arquivo), len(pastas)))
print("=" * 100)

sem_arquivo = []
for chave, info in sorted(pastas.items()):
    if info['nome'] not in cidades_com_arquivo:
        sem_arquivo.append((info['nome_amigavel'], info['nome']))

for nome_amigavel, nome in sem_arquivo:
    print("  FALTA: {} -> resultados_{}.csv".format(nome_amigavel, nome))

print("\n" + "=" * 100)
print("SOLUCAO: Executar processamento paralelo para cada cidade")
print("=" * 100)
