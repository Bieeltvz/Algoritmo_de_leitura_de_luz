import requests
import json

BASE_URL = "http://localhost:5000"

# 1. Testar listar pastas
print("1. Listando pastas disponíveis...")
resp = requests.get(f"{BASE_URL}/api/listar-pastas")
pastas_dict = resp.json()
print(f"   Tipo de resposta: {type(pastas_dict)}")
print(f"   Pastas disponíveis: {pastas_dict}")

# Se for um dict com pastas como values
if isinstance(pastas_dict, dict):
    pastas = list(pastas_dict.values()) if pastas_dict else []
else:
    pastas = pastas_dict if isinstance(pastas_dict, list) else []

print(f"   Total: {len(pastas)} pastas")

if pastas:
    # Selecionar a primeira
    pasta_selecionada = pastas[0]
    print(f"   Selecionando: {pasta_selecionada}")
    
    # 2. Selecionar pasta
    print("\n2. Selecionando pasta...")
    resp = requests.post(f"{BASE_URL}/api/selecionar-pasta", json=pasta_selecionada)
    resultado = resp.json()
    print(f"   Resultado: {resultado}")
    
    # 3. Testar tendências
    print("\n3. Solicitando tendências...")
    resp = requests.get(f"{BASE_URL}/api/tendencias")
    tendencias = resp.json()
    print(f"   Resposta: {json.dumps(tendencias, indent=2)}")
    
    if tendencias.get('sucesso'):
        print(f"   Total de anos: {len(tendencias.get('tendencias', []))}")
    else:
        print(f"   ❌ Erro: {tendencias.get('mensagem', 'Desconhecido')}")
