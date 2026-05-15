"""
Script para debug - examina estrutura dos dados do IBGE
"""

import requests
import json

print("🔍 Buscando dados de alguns municípios de SC...")

# Buscar alguns exemplos
url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SC/municipios"
response = requests.get(url)
municipios = response.json()

print(f"\nTotal de municípios em SC: {len(municipios)}")
print("\n" + "="*80)
print("PRIMEIROS 3 MUNICÍPIOS:")
print("="*80 + "\n")

for mun in municipios[:3]:
    print(f"Nome: {mun.get('nome')}")
    print(f"ID: {mun.get('id')}")
    print(f"Chave: {mun.get('nome-simplificado') if 'nome-simplificado' in mun else 'N/A'}")
    print(f"Todas as chaves: {list(mun.keys())}")
    print()

# Agora tenta buscar dados detalhados com geometria
print("\n" + "="*80)
print("BUSCANDO GEOMETRIA DE UM MUNICÍPIO:")
print("="*80 + "\n")

# Procurar Bombinhas
target = "Bombinhas"
for mun in municipios:
    if target.lower() in mun.get('nome', '').lower():
        print(f"Encontrado: {mun['nome']} (ID: {mun['id']})")
        
        # Buscar dados com geometria
        url_geo = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{mun['id']}"
        response = requests.get(url_geo)
        dados = response.json()
        
        print(f"\nChaves disponíveis: {list(dados.keys())}")
        print(f"\nDados completos:")
        print(json.dumps(dados, indent=2, ensure_ascii=False))
        break

# Tentar buscar lista com geometria
print("\n" + "="*80)
print("TESTANDO COM PARÂMETRO ?formato=json&geometria=true:")
print("="*80 + "\n")

url_teste = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SC/municipios?formato=json&geometria=true"
try:
    response = requests.get(url_teste, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Tamanho da resposta: {len(response.text)} bytes")
    
    # Verificar primeiros 500 caracteres
    print(f"\nPrimeiros 500 caracteres:")
    print(response.text[:500])
except Exception as e:
    print(f"Erro: {e}")

# Tentar outros endpoints
print("\n" + "="*80)
print("ENDPOINTS DISPONÍVEIS DO IBGE:")
print("="*80 + "\n")

endpoints = [
    "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SC",
    "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SC/municipios",
]

for endpoint in endpoints:
    try:
        r = requests.head(endpoint)
        print(f"✓ {endpoint} -> {r.status_code}")
    except:
        print(f"✗ {endpoint} -> ERRO")
