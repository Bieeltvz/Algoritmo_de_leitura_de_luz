"""
Script para obter coordenadas oficiais do IBGE para cidades de Santa Catarina

O IBGE fornece coordenadas precisas do centroide de cada município,
que são mais confiáveis que dados do Nominatim/OpenStreetMap

API: https://servicodados.ibge.gov.br/api/v1/localidades/municipios/
"""

import requests
import json
import unicodedata
from pathlib import Path

def remove_accents(text):
    """Remove accents from text and convert to lowercase"""
    nfd_form = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd_form if unicodedata.category(char) != 'Mn').lower()

# Lista de cidades de Santa Catarina
cidades_sc = [
    "Bombinhas", "Balneário Camboriú", "Picarras", "Penha", "Porto Belo",
    "Ilhota", "Itajaí", "Itapema", "Navegantes", "Tijucas",
    "Bom Retiro do Sul", "Barra Velha", "Brusque", "Gaspar", "Blumenau",
    "Pomerode", "Botuverá", "Guabiruba", "Luiz Alves", "Agronomica",
    "Dona Emma", "Mirim Doce", "Doutor Pedrinho", "Witmarsum", "Canelinha",
    "Benedito Novo", "Leoberto Leal", "Indaial", "Timbó", "Ibirama",
    "Apiúna", "Rodeio", "Rio dos Cedros", "Chapadão do Lageado", "Ascurra",
    "Guide", "Laurentino", "Nova Trento", "Imbuia", "Lontras",
    "Vidal Ramos", "José Boiteux", "Rio do Campo", "Agrolandia", "Atlanta",
    "Petrolândia", "Presidente Nereu", "Braco do Trombudo", "Trombudo Central",
    "Rio do Oeste", "Pouso Redondo", "Salete", "Presidente Getúlio", "Taió",
    "Aurora", "Ituparanga", "Santa Terezinha", "São João Batista"
]

def obter_municipios_sc():
    """Obtém lista de todos os municípios de SC do IBGE"""
    try:
        print("🔍 Buscando lista de municípios de SC no IBGE...")
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SC/municipios"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Erro ao buscar municípios: {e}")
        return []

def encontrar_coordenadas_ibge(cidade_nome, municipios_sc):
    """
    Encontra coordenadas de uma cidade na lista de municípios do IBGE
    Retorna (latitude, longitude)
    """
    cidade_normalizada = remove_accents(cidade_nome)
    
    for municipio in municipios_sc:
        nome_municipio_normalizado = remove_accents(municipio.get('nome', ''))
        
        if cidade_normalizada in nome_municipio_normalizado or nome_municipio_normalizado in cidade_normalizada:
            geo = municipio.get('microrregiao', {}).get('mesorregiao', {}).get('UF', {})
            
            # Tenta obter geometria do município
            try:
                municipio_id = municipio.get('id')
                if municipio_id:
                    url_geo = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{municipio_id}"
                    response = requests.get(url_geo, timeout=5)
                    dados = response.json()
                    
                    # Extrai as coordenadas
                    geometria = dados.get('geometria', {})
                    if geometria and 'centroide' in geometria:
                        centroide = geometria['centroide']['coordinates']
                        # IBGE retorna [longitude, latitude]
                        lat, lng = centroide[1], centroide[0]
                        return (lat, lng)
            except Exception as e:
                print(f"  ⚠️ Erro ao buscar geometria para {municipio_id}: {e}")
    
    return None

def main():
    print("=" * 80)
    print("🌍 OBTENDO COORDENADAS DO IBGE - CIDADES DE SANTA CATARINA")
    print("=" * 80)
    print()
    
    # Obter todos os municípios de SC
    municipios_sc = obter_municipios_sc()
    
    if not municipios_sc:
        print("❌ Não foi possível obter dados do IBGE")
        return
    
    print(f"✓ {len(municipios_sc)} municípios de SC carregados do IBGE\n")
    
    coordenadas_ibge = {}
    coordenadas_python = {}
    falhadas = []
    
    print("Buscando coordenadas...")
    print("-" * 80)
    
    for i, cidade in enumerate(cidades_sc, 1):
        print(f"[{i}/{len(cidades_sc)}] {cidade}...", end=" ", flush=True)
        
        coords = encontrar_coordenadas_ibge(cidade, municipios_sc)
        
        if coords:
            lat, lng = coords
            chave_normalizada = remove_accents(cidade)
            
            # Formato JSON
            coordenadas_ibge[cidade] = [lat, lng]
            
            # Formato Python dict (para app.py)
            coordenadas_python[chave_normalizada] = (lat, lng)
            
            print(f"✓ ({lat:.4f}, {lng:.4f})")
        else:
            print("❌ NÃO ENCONTRADA")
            falhadas.append(cidade)
    
    print("\n" + "=" * 80)
    print("RESULTADOS")
    print("=" * 80)
    
    # Salvar em JSON
    output_json = "coordenadas_cidades_ibge.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(coordenadas_ibge, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Coordenadas salvas em: {output_json}")
    
    # Gerar formato Python
    print("\n📝 FORMATO PYTHON DICT (para app.py):")
    print("-" * 80)
    print("\nCOORDENADAS_CIDADES_IBGE = {")
    for chave in sorted(coordenadas_python.keys()):
        lat, lng = coordenadas_python[chave]
        print(f'    "{chave}": ({lat:.4f}, {lng:.4f}),')
    print("}")
    
    # Estatísticas
    print("\n" + "=" * 80)
    print(f"✅ {len(coordenadas_ibge)} cidades encontradas")
    if falhadas:
        print(f"❌ {len(falhadas)} cidades não encontradas:")
        for cidade in falhadas:
            print(f"   - {cidade}")
    print("=" * 80)

if __name__ == "__main__":
    main()
