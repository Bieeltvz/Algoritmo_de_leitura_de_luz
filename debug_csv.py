"""
Debug: Verificar se a app consegue ler o CSV
"""

import csv
from pathlib import Path

# Simular o que a app.py faz
nome_cidade = "Canelinha_recortes"
arquivo_csv = Path(f'resultados_{nome_cidade}.csv')

print(f"Procurando por: {arquivo_csv}")
print(f"Arquivo existe? {arquivo_csv.exists()}")

if arquivo_csv.exists():
    print(f"Tamanho: {arquivo_csv.stat().st_size} bytes")
    
    # Tentar ler
    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        print(f"✓ Lido com sucesso!")
        print(f"Total de registros: {len(rows)}")
        
        if rows:
            print(f"\nPrimeiro registro:")
            for k, v in list(rows[0].items())[:6]:
                print(f"  {k}: {v}")
            
            # Tentar converter para float
            try:
                media = float(rows[0]['intensidade_media'])
                print(f"\nMedia em float: {media}")
            except Exception as e:
                print(f"ERRO ao converter media: {e}")
    except Exception as e:
        print(f"✗ Erro ao ler: {e}")
else:
    print("✗ Arquivo não encontrado!")
    print("\nArquivos disponíveis:")
    for f in Path('.').glob('resultados_*.csv'):
        print(f"  - {f.name}")
