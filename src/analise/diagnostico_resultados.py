#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar quais cidades têm resultados
"""

from pathlib import Path
import json
import csv

DIRETORIO_TRABALHO = Path(__file__).parent.absolute()

print("=" * 100)
print("DIAGNÓSTICO: VERIFICANDO RESULTADOS POR CIDADE")
print("=" * 100)

# Listar todas as cidades
cidades_com_csv = {}
cidades_sem_csv = {}

# Buscar todos os arquivos resultados_*.csv
for arquivo_csv in DIRETORIO_TRABALHO.glob('resultados_*.csv'):
    nome_cidade = arquivo_csv.stem.replace('resultados_', '')
    
    # Verificar tamanho e conteúdo
    tamanho = arquivo_csv.stat().st_size
    
    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            linhas = list(reader)
            
        cidades_com_csv[nome_cidade] = {
            'arquivo': arquivo_csv.name,
            'tamanho': tamanho,
            'registros': len(linhas),
            'status': 'OK' if len(linhas) > 0 else 'CSV VAZIO'
        }
    except Exception as e:
        cidades_com_csv[nome_cidade] = {
            'arquivo': arquivo_csv.name,
            'tamanho': tamanho,
            'registros': 0,
            'status': f'ERRO: {e}'
        }

# Agora verificar quais cidades são descobertas mas não têm CSV
import sys
sys.path.insert(0, str(DIRETORIO_TRABALHO))
from app import descobrir_pastas_cidades

pastas = descobrir_pastas_cidades()

print(f"\n[1] CIDADES DESCOBERTAS: {len(pastas)}")
print(f"[2] CIDADES COM ARQUIVO CSV: {len(cidades_com_csv)}")
print(f"[3] CIDADES SEM ARQUIVO CSV: {len(pastas) - len(cidades_com_csv)}")

print("\n" + "=" * 100)
print("DETALHES POR CIDADE:")
print("=" * 100)

for chave, info in sorted(pastas.items()):
    cidade_nome = info['nome']
    
    if cidade_nome in cidades_com_csv:
        csv_info = cidades_com_csv[cidade_nome]
        print(f"\n✓ {info['nome_amigavel']}")
        print(f"  Arquivo: {csv_info['arquivo']}")
        print(f"  Registros: {csv_info['registros']}")
        print(f"  Status: {csv_info['status']}")
    else:
        print(f"\n✗ {info['nome_amigavel']}")
        print(f"  ARQUIVO FALTANDO: resultados_{cidade_nome}.csv")

print("\n" + "=" * 100)
print("RESUMO:")
print("=" * 100)

# Agrupar por status
with_results = sum(1 for v in cidades_com_csv.values() if v['registros'] > 0)
without_results = sum(1 for v in cidades_com_csv.values() if v['registros'] == 0)
no_csv = len(pastas) - len(cidades_com_csv)

print(f"\nCidades com resultados: {with_results}")
print(f"Cidades com CSV vazio: {without_results}")
print(f"Cidades sem arquivo CSV: {no_csv}")

# Mostrar cidades sem arquivo
if no_csv > 0:
    print(f"\n❌ Cidades SEM arquivo resultados_*.csv:")
    for chave, info in sorted(pastas.items()):
        if info['nome'] not in cidades_com_csv:
            print(f"   - {info['nome_amigavel']}")
            print(f"     Esperado: resultados_{info['nome']}.csv")
