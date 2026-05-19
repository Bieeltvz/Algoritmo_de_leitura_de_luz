#!/usr/bin/env python3
"""
Debug: Braco Do Trombudo - Encontrar por que não está funcionando
"""

from mapa_crescimento import MapaCrescimento
import json
from pathlib import Path

m = MapaCrescimento()

print("=== Debug: Braco Do Trombudo ===\n")

# Carregar coordenadas
m.carregar_coordenadas()

print("Cidades disponíveis com 'trombudo':")
for chave in sorted(m.coordenadas.keys()):
    if 'trombudo' in chave.lower():
        print(f"  '{chave}' → {m.coordenadas[chave]}")

print("\n" + "="*50 + "\n")

# Tentar diferentes variações do nome
nomes_teste = [
    'Braco Do Trombudo',
    'braco do trombudo',
    'Braco_Do_Trombudo',
    'Braco_do_Trombudo',
    'Braco Do Trombudos',
    'Braco_Do_Trombudos',
]

print("Testando diferentes nomes:")
for nome_teste in nomes_teste:
    print(f"\n  Nome: '{nome_teste}'")
    
    # Tentar encontrar dados de crescimento
    dados = m.calcular_crescimento_cidade_unica(nome_teste)
    if dados:
        print(f"    ✅ Encontrado: {dados['nome']}")
    else:
        print(f"    ❌ Não encontrado")
    
    # Tentar encontrar no encontrar_arquivo_csv
    csv_path = m.encontrar_arquivo_csv(nome_teste)
    if csv_path:
        print(f"    ✅ CSV: {csv_path}")
    else:
        print(f"    ❌ CSV não encontrado")

print("\n" + "="*50 + "\n")

# Listar todos os arquivos processados_* que contêm "Braco"
print("Arquivos de saída que contêm 'Braco':")
base_path = Path(__file__).parent.absolute()
for f in sorted(base_path.glob('processados_*Braco*.json')):
    print(f"  {f.name}")

print("\nArquivos de resultado que contêm 'Braco':")
for f in sorted(base_path.glob('resultados_*Braco*.csv')):
    print(f"  {f.name}")

print("\n" + "="*50 + "\n")

# Procurar arquivos processados para Braco
print("Conteúdo de processados_Braco_Do_Trombudo_recortes.json (primeiras 2 entradas):")
arquivo = base_path / 'processados_Braco_Do_Trombudo_recortes.json'
if arquivo.exists():
    with open(arquivo) as f:
        dados = json.load(f)
        print(f"  Total de entradas: {len(dados)}")
        # Mostrar estrutura
        if dados:
            primeira = list(dados.items())[0]
            print(f"  Exemplo: {primeira[0]}")
            print(f"  Campos: {list(primeira[1].keys()) if isinstance(primeira[1], dict) else 'array'}")
else:
    print(f"  ❌ Arquivo não encontrado")

print("\n" + "="*50 + "\n")

# Procurar pelos resultados CSV
print("Testando findCsv para 'Braco_Do_Trombudo':")
csv_path = m.encontrar_arquivo_csv('Braco_Do_Trombudo')
print(f"  Resultado: {csv_path}")

if csv_path:
    import pandas as pd
    df = pd.read_csv(csv_path)
    print(f"  Linhas: {len(df)}")
    print(f"  Anos únicos: {sorted(df['ano'].unique())}")
    print(f"  Intensidade média: {df['intensidade_media'].mean():.2f}")
