import csv

rows = list(csv.DictReader(open('resultados_padrao.csv')))
print('Análise dos 5 primeiros registros:\n')
print('Arquivo | Media Bruta | Desvio Bruto | Median Bruta | Threshold Bruto | % Válida')
print('-' * 80)
for row in rows[:5]:
    media = float(row["intensidade_media"])
    desvio = float(row["desvio"])
    mediana = float(row["mediana"])
    threshold = (media + 0.5 * desvio)
    valid = row["percentual_valido"]
    print(f"{row['arquivo']:25} | {media:11.4f} | {desvio:12.4f} | {mediana:12.4f} | {threshold:15.4f} | {valid}%")

print('\nResumo:')
all_media = [float(r["intensidade_media"]) for r in rows]
all_desvio = [float(r["desvio"]) for r in rows]
print(f"Media geral (bruta): {sum(all_media)/len(all_media):.4f}")
print(f"Desvio médio: {sum(all_desvio)/len(all_desvio):.4f}")
print(f"Min media: {min(all_media):.4f}")
print(f"Max media: {max(all_media):.4f}")
print(f"Min desvio: {min(all_desvio):.4f}")
print(f"Max desvio: {max(all_desvio):.4f}")
