#!/usr/bin/env python3
"""
Debug: Simular exatamente o que app.py faz quando clica em 'Gerar Mapa Interativo'
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento
import logging
import sys
import io

# UTF-8 encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

print("=" * 70)
print("Simulando: app.py → /api/gerar-mapa-crescimento")
print("=" * 70)

# Simular PASTA_SELECIONADA do app.py
PASTA_SELECIONADA = {
    'nome': 'Braco_Do_Trombudo_recortes',  # Como vem de PASTAS_DISPONIVEIS
    'nome_amigavel': 'Braco Do Trombudo - Braco Do Trombudos'
}

DIRETORIO_TRABALHO = Path(__file__).parent.absolute()

print(f"\nPASTAS_SELECIONADA['nome']: {PASTA_SELECIONADA['nome']}")
print(f"PASTA_SELECIONADA['nome_amigavel']: {PASTA_SELECIONADA['nome_amigavel']}")

# Passo 1: Criar MapaCrescimento
print("\n[1] Criando MapaCrescimento...")
mapa = MapaCrescimento()

# Passo 2: Carregar coordenadas
print("[2] Carregando coordenadas...")
if not mapa.carregar_coordenadas():
    print("    ERRO: Falha ao carregar coordenadas!")
    sys.exit(1)

# Passo 3: Chamar gerar_relatorio_html_cidade
nome_cidade = PASTA_SELECIONADA['nome']
nome_amigavel = PASTA_SELECIONADA['nome_amigavel']

print(f"\n[3] Chamando gerar_relatorio_html_cidade('{nome_cidade}')")
arquivo_html = DIRETORIO_TRABALHO / f'mapa_{nome_cidade}.html'

print(f"    Arquivo de saída: {arquivo_html}")

arquivo_gerado = mapa.gerar_relatorio_html_cidade(nome_cidade, str(arquivo_html))

print(f"    Resultado: {arquivo_gerado}")

if not arquivo_gerado:
    print("\n    PROBLEMA: gerar_relatorio_html_cidade retornou None/False")
    print("    Isto significa que calcular_crescimento_cidade_unica retornou dict vazio")
    
    # Debugar passo a passo
    print("\n[4] Debugando calcular_crescimento_cidade_unica...")
    
    # Encontrar CSV
    csv_path = mapa.encontrar_arquivo_csv(nome_cidade)
    print(f"    CSV encontrado: {csv_path}")
    
    if csv_path:
        # Tentar calcular manualmente
        import csv as csv_module
        with open(csv_path) as f:
            reader = csv_module.DictReader(f)
            dados = list(reader)
            print(f"    Linhas do CSV: {len(dados)}")
            if dados:
                print(f"    Primeira linha: {dados[0]}")
        
        # Tentar calcular crescimento
        resultado = mapa.calcular_crescimento_cidade_unica(nome_cidade)
        print(f"    Resultado: {resultado}")
        
        if not resultado:
            print("\n    Possível problema:")
            print("    - Coordenadas não encontradas? Testando...")
            
            nome_exibicao = nome_cidade.replace('_', ' ')
            nome_busca = nome_exibicao.lower()
            for sufixo in ['recorte', 'recortes', 'recortado', 'reprojetado', 'noturno', 'noturna']:
                nome_busca = nome_busca.replace(f' {sufixo}', '')
            
            print(f"      Nome para buscar: '{nome_busca}'")
            print(f"      Cidades com 'braco': {[k for k in mapa.coordenadas.keys() if 'braco' in k.lower()]}")

else:
    print("\n✅ SUCESSO! Mapa gerado com sucesso!")
    if Path(arquivo_html).exists():
        tamanho_kb = Path(arquivo_html).stat().st_size / 1024
        print(f"    Arquivo: {arquivo_html}")
        print(f"    Tamanho: {tamanho_kb:.1f} KB")
