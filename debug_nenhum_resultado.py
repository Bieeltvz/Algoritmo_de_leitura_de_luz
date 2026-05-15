#!/usr/bin/env python3
"""
Debug específico: Por que calcular_crescimento_cidade_unica falha para Braco_Do_Trombudo
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

m = MapaCrescimento()
m.carregar_coordenadas()

print("=== Debug: Braco_Do_Trombudo ===\n")

# Teste 1: Encontrar CSV
print("Teste 1: encontrar_arquivo_csv('Braco_Do_Trombudo')")
csv_path = m.encontrar_arquivo_csv('Braco_Do_Trombudo')
print(f"  Resultado: {csv_path}")

if csv_path:
    # Teste 2: Ler o arquivo
    import pandas as pd
    print("\nTeste 2: Ler dados do CSV")
    try:
        df = pd.read_csv(csv_path)
        print(f"  Linhas: {len(df)}")
        print(f"  Anos: {sorted(df['ano'].unique())}")
        print(f"  Colunas: {df.columns.tolist()}")
    except Exception as e:
        print(f"  Erro: {e}")

# Teste 3: Procurar coordenadas
print("\nTeste 3: Procurar coordenadas")
print(f"  Total de cidades no dict: {len(m.coordenadas)}")

# Listar cidades com 'trombudo'
encontradas = [k for k in m.coordenadas.keys() if 'trombudo' in k.lower()]
print(f"  Cidades com 'trombudo': {encontradas}")

# Procurar 'braco'
encontradas_braco = [k for k in m.coordenadas.keys() if 'braco' in k.lower()]
print(f"  Cidades com 'braco': {encontradas_braco}")

# Teste 4: Chamar calcular_crescimento_cidade_unica
print("\nTeste 4: calcular_crescimento_cidade_unica('Braco_Do_Trombudo')")
resultado = m.calcular_crescimento_cidade_unica('Braco_Do_Trombudo')
print(f"  Resultado: {resultado}")

if not resultado:
    print("\n  PROBLEMA: Nenhum resultado!")
    print("  Debugando passo a passo...")
    
    # Verificar CSV novamente
    csv = m.encontrar_arquivo_csv('Braco_Do_Trombudo')
    print(f"    CSV: {csv}")
    
    if csv:
        import pandas as pd
        df = pd.read_csv(csv)
        print(f"    Dados CSV carregados OK ({len(df)} linhas)")
        
        # Verificar coordenada
        nome_busca = 'Braco_Do_Trombudo'.replace('_', ' ').lower()
        print(f"    Procurando por: '{nome_busca}'")
        
        for chave in m.coordenadas.keys():
            if nome_busca in chave.lower() or chave.lower() in nome_busca:
                print(f"      Match potencial: '{chave}' -> {m.coordenadas[chave]}")
