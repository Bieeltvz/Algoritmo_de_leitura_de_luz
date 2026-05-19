#!/usr/bin/env python3
import csv
import os

# Ler o arquivo original
src_file = 'resultados_padrao.csv'
dst_file = 'resultados_Canelinha_recortes.csv'

print(f"Lendo: {src_file}")
with open(src_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"Total de linhas: {len(rows)}")

# Converter valores
campos_converter = ['intensidade_media', 'mediana', 'desvio', 'threshold_crescimento']

for row in rows:
    for campo in campos_converter:
        if campo in row and row[campo]:
            try:
                val = float(row[campo])
                row[campo] = str(val * 255)
            except:
                pass

# Salvar
print(f"Salvando em: {dst_file}")
with open(dst_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Verificar
file_size = os.path.getsize(dst_file)
print(f"✓ Arquivo criado: {file_size} bytes")
print(f"✓ Total de registros: {len(rows)}")

# Mostrar primeiros valores
print("\nPrimeiros 3 valores de media (convertidos):")
for i, row in enumerate(rows[:3]):
    print(f"  {i+1}. {row.get('arquivo', 'N/A')}: {row.get('intensidade_media', 'N/A')}")
