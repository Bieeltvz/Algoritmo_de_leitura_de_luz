import csv

rows = list(csv.DictReader(open('resultados_padrao.csv')))
print('Primeiros 3 registros originais:')
for i, row in enumerate(rows[:3]):
    print(f'{i+1}. {row["arquivo"]}: media={row["intensidade_media"]}, mediana={row["mediana"]}, desvio={row["desvio"]}')
