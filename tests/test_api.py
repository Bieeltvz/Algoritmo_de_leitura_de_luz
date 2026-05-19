import requests

# Primeiro, seleciona a pasta Canelinha
response = requests.post('http://localhost:5000/api/selecionar-pasta', json={'nome_pasta': 'Canelinhas'})
print('Pasta selecionada:')
print(response.json())

print('\n---\n')

# Depois pede os resultados
response = requests.get('http://localhost:5000/api/resultados')
data = response.json()
print(f'Status: {data.get("sucesso")}')
print(f'Total de registros: {data.get("total_registros")}')
print(f'Média geral: {data.get("media_geral")}')
print(f'Mínimo: {data.get("minimo")}')
print(f'Máximo: {data.get("maximo")}')

if data.get('resultados'):
    print(f'\nPrimeiro resultado:')
    primeiro = data['resultados'][0]
    print(f'  Arquivo: {primeiro.get("arquivo")}')
    print(f'  Media: {primeiro.get("intensidade_media")}')
    print(f'  Válido %: {primeiro.get("percentual_valido")}')
    
    print(f'\nÚltimo resultado:')
    ultimo = data['resultados'][-1]
    print(f'  Arquivo: {ultimo.get("arquivo")}')
    print(f'  Media: {ultimo.get("intensidade_media")}')
    print(f'  Válido %: {ultimo.get("percentual_valido")}')
