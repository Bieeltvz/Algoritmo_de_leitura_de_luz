#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste direto do mapa para Braco Do Trombudo
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento
import os

# Mudar para o diretório correto
os.chdir(Path(__file__).parent)

mapa = MapaCrescimento()
mapa.carregar_coordenadas()

nome_cidade = "Braco_Do_Trombudo_recortes"
arquivo_mapa = f'mapa_{nome_cidade}.html'

print(f"Gerando mapa para {nome_cidade}...")
resultado = mapa.gerar_relatorio_html_cidade(nome_cidade, arquivo_mapa)

if resultado:
    tamanho = Path(resultado).stat().st_size / 1024
    print(f"SUCESSO! Mapa gerado: {resultado} ({tamanho:.1f} KB)")
else:
    print(f"ERRO! Mapa nao gerado")
    print(f"Coordenadas carregadas: {len(mapa.coordenadas)}")
    
    # Debug
    nome_busca = nome_cidade.replace('_', ' ').lower()
    for sufixo in ['recortes', 'recorte', 'recortado', 'reprojetado', 'reprojet', 'noturno', 'noturna']:
        nome_busca = nome_busca.replace(f' {sufixo}', '').replace(f'_{sufixo}', '')
    print(f"Nome busca: {nome_busca}")
    
    matching_keys = [k for k in mapa.coordenadas if k.lower() == nome_busca]
    print(f"Chaves encontradas: {matching_keys}")
