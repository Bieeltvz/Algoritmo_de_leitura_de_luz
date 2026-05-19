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

# Sem conversão - manter valores em escala bruta (0-1)
# Os valores já estão na escala correta

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

# Mostrar primeiros valores (escala bruta)
print("\nPrimeiros 3 valores (escala bruta 0-1):")
for i, row in enumerate(rows[:3]):
    media = float(row.get('intensidade_media', 0))
    threshold = (media + 0.5 * float(row.get('desvio', 0)))
    print(f"  {i+1}. {row.get('arquivo', 'N/A')}: media={media:.4f}, threshold={threshold:.4f}")

