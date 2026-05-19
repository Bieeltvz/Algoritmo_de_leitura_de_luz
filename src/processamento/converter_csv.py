#!/usr/bin/env python3
"""
Converte resultados_padrao.csv multiplicando valores por 255
Cria resultados_Canelinha_recortes.csv com valores corretos
"""

import csv
from pathlib import Path

input_file = Path('resultados_padrao.csv')
output_file = Path('resultados_Canelinha_recortes.csv')

if not input_file.exists():
    print(f"ERRO: {input_file} não encontrado")
    exit(1)

print(f"Convertendo {input_file.name}...")
print(f"Multiplicando por 255...")

# Campos numéricos que precisam ser multiplicados por 255
numeric_fields = ['intensidade_media', 'mediana', 'desvio', 'threshold_crescimento']

rows_converted = 0

with open(input_file) as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    
    writer.writeheader()
    
    for row in reader:
        # Converter campos numéricos
        for field in numeric_fields:
            if field in row:
                try:
                    valor = float(row[field])
                    row[field] = f"{valor * 255:.2f}"
                except:
                    pass
        
        writer.writerow(row)
        rows_converted += 1

print(f"\n✓ Convertido {rows_converted} registros")
print(f"✓ Salvo em: {output_file}")

# Verificar resultado
print(f"\nVerificação:")
with open(output_file) as f:
    rows = list(csv.DictReader(f))
    print(f"Total: {len(rows)} registros")
    print(f"Primeiros 3 valores de media:")
    for i, r in enumerate(rows[:3], 1):
        print(f"  {i}. {r['arquivo']}: {r['intensidade_media']}")
