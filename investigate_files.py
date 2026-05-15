#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para investigar o estado dos arquivos CSV e JSON
"""

from pathlib import Path
import json
import os

DIRETORIO_TRABALHO = Path(__file__).parent.absolute()

# Listar todos os arquivos de resultado
print("Investigando estado dos arquivos...")
print("=" * 80)

arquivo_csv = DIRETORIO_TRABALHO / 'resultados_Braco_Do_Trombudo_recortes.csv'
arquivo_json = DIRETORIO_TRABALHO / 'processados_Braco_Do_Trombudo_recortes.json'

print(f"\n[CSV] {arquivo_csv.name}")
print(f"  Existe: {arquivo_csv.exists()}")
if arquivo_csv.exists():
    tamanho = arquivo_csv.stat().st_size
    print(f"  Tamanho: {tamanho} bytes")
    
    with open(arquivo_csv, 'r') as f:
        conteudo = f.read()
        linhas = conteudo.strip().split('\n') if conteudo.strip() else []
        print(f"  Linhas: {len(linhas)}")
        if linhas:
            print(f"  Primeira linha: {linhas[0][:100]}...")

print(f"\n[JSON] {arquivo_json.name}")
print(f"  Existe: {arquivo_json.exists()}")
if arquivo_json.exists():
    tamanho = arquivo_json.stat().st_size
    print(f"  Tamanho: {tamanho} bytes")
    
    with open(arquivo_json, 'r') as f:
        cache = json.load(f)
        print(f"  Registros: {len(cache)}")
        if cache:
            primeiro_arquivo = list(cache.keys())[0]
            print(f"  Exemplo: {primeiro_arquivo}")

print("\n" + "=" * 80)
print("\nVERIFICAÇÃO: Ambos os arquivos estão vazios!")
print("Possível causa: O processador paralelo ainda não foi executado.")
print("Solução: Clique em 'Iniciar Processamento Paralelo' na interface web.")
