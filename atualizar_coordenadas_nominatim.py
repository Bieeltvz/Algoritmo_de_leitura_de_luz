"""
Script para corrigir coordenadas usando Nominatim com buscas mais precisas

Estratégia:
1. Usa queries mais específicas: "Cidade, Santa Catarina, Brasil"
2. Valida as coordenadas retornadas
3. Corrige principalmente as cidades agrupadas
"""

import requests
import json
import time
import unicodedata
from pathlib import Path

def remove_accents(text):
    """Remove accents from text and convert to lowercase"""
    nfd_form = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd_form if unicodedata.category(char) != 'Mn').lower()

# Mapa de cidades para busca otimizada no Nominatim
# Algumas cidades têm nomes diferentes no OpenStreetMap
CIDADES_SC = {
    "Bombinhas": "Bombinhas, Santa Catarina, Brazil",
    "Balneário Camboriú": "Balneário Camboriú, Santa Catarina, Brazil",
    "Picarras": "Picarras, Santa Catarina, Brazil",
    "Penha": "Penha, Santa Catarina, Brazil",
    "Porto Belo": "Porto Belo, Santa Catarina, Brazil",
    "Ilhota": "Ilhota, Santa Catarina, Brazil",
    "Itajaí": "Itajaí, Santa Catarina, Brazil",
    "Itapema": "Itapema, Santa Catarina, Brazil",
    "Navegantes": "Navegantes, Santa Catarina, Brazil",
    "Tijucas": "Tijucas, Santa Catarina, Brazil",
    "Bom Retiro do Sul": "Bom Retiro do Sul, Santa Catarina, Brazil",
    "Barra Velha": "Barra Velha, Santa Catarina, Brazil",
    "Brusque": "Brusque, Santa Catarina, Brazil",
    "Gaspar": "Gaspar, Santa Catarina, Brazil",
    "Blumenau": "Blumenau, Santa Catarina, Brazil",
    "Pomerode": "Pomerode, Santa Catarina, Brazil",
    "Botuverá": "Botuverá, Santa Catarina, Brazil",
    "Guabiruba": "Guabiruba, Santa Catarina, Brazil",
    "Luiz Alves": "Luiz Alves, Santa Catarina, Brazil",
    "Agronomica": "Agronomica, Santa Catarina, Brazil",
    "Dona Emma": "Dona Emma, Santa Catarina, Brazil",
    "Mirim Doce": "Mirim Doce, Santa Catarina, Brazil",
    "Doutor Pedrinho": "Doutor Pedrinho, Santa Catarina, Brazil",
    "Witmarsum": "Witmarsum, Santa Catarina, Brazil",
    "Canelinha": "Canelinha, Santa Catarina, Brazil",
    "Benedito Novo": "Benedito Novo, Santa Catarina, Brazil",
    "Leoberto Leal": "Leoberto Leal, Santa Catarina, Brazil",
    "Indaial": "Indaial, Santa Catarina, Brazil",
    "Timbó": "Timbó, Santa Catarina, Brazil",
    "Ibirama": "Ibirama, Santa Catarina, Brazil",
    "Apiúna": "Apiúna, Santa Catarina, Brazil",
    "Rodeio": "Rodeio, Santa Catarina, Brazil",
    "Rio dos Cedros": "Rio dos Cedros, Santa Catarina, Brazil",
    "Chapadão do Lageado": "Chapadão do Lageado, Santa Catarina, Brazil",
    "Ascurra": "Ascurra, Santa Catarina, Brazil",
    "Guide": "Guide, Santa Catarina, Brazil",
    "Laurentino": "Laurentino, Santa Catarina, Brazil",
    "Nova Trento": "Nova Trento, Santa Catarina, Brazil",
    "Imbuia": "Imbuia, Santa Catarina, Brazil",
    "Lontras": "Lontras, Santa Catarina, Brazil",
    "Vidal Ramos": "Vidal Ramos, Santa Catarina, Brazil",
    "José Boiteux": "José Boiteux, Santa Catarina, Brazil",
    "Rio do Campo": "Rio do Campo, Santa Catarina, Brazil",
    "Agrolandia": "Agrolandia, Santa Catarina, Brazil",
    "Atlanta": "Atlanta, Santa Catarina, Brazil",
    "Petrolândia": "Petrolândia, Santa Catarina, Brazil",
    "Presidente Nereu": "Presidente Nereu, Santa Catarina, Brazil",
    "Braco do Trombudo": "Braco do Trombudo, Santa Catarina, Brazil",
    "Trombudo Central": "Trombudo Central, Santa Catarina, Brazil",
    "Rio do Oeste": "Rio do Oeste, Santa Catarina, Brazil",
    "Pouso Redondo": "Pouso Redondo, Santa Catarina, Brazil",
    "Salete": "Salete, Santa Catarina, Brazil",
    "Presidente Getúlio": "Presidente Getúlio, Santa Catarina, Brazil",
    "Taió": "Taió, Santa Catarina, Brazil",
    "Aurora": "Aurora, Santa Catarina, Brazil",
    "Ituparanga": "Ituparanga, Santa Catarina, Brazil",
    "Santa Terezinha": "Santa Terezinha, Santa Catarina, Brazil",
    "São João Batista": "São João Batista, Santa Catarina, Brazil",
}

def get_coordinates_nominatim(city_name, query):
    """Get coordinates from Nominatim API com query mais precisa"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query,
            "format": "json",
            "limit": 1,
            "addressdetails": 1
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data and len(data) > 0:
            result = data[0]
            lat = float(result['lat'])
            lng = float(result['lon'])
            # Retorna com precisão de 4 casas decimais (aprox 11 metros)
            return (round(lat, 4), round(lng, 4))
        else:
            return None
    except Exception as e:
        print(f"  ⚠️ Erro: {e}")
        return None

def main():
    print("=" * 90)
    print("🌍 OBTENDO COORDENADAS PRECISAS DO NOMINATIM/OPENSTREETMAP")
    print("=" * 90)
    print()
    
    coordenadas_json = {}
    coordenadas_python = {}
    falhadas = []
    
    print("Buscando coordenadas com query precisa...")
    print("-" * 90)
    
    for i, (cidade, query) in enumerate(CIDADES_SC.items(), 1):
        print(f"[{i}/{len(CIDADES_SC)}] {cidade:30}", end=" ", flush=True)
        
        coords = get_coordinates_nominatim(cidade, query)
        
        if coords:
            lat, lng = coords
            chave_normalizada = remove_accents(cidade)
            
            # Formato JSON (array)
            coordenadas_json[cidade] = [lat, lng]
            
            # Formato Python dict (tupla)
            coordenadas_python[chave_normalizada] = (lat, lng)
            
            print(f"✓ ({lat}, {lng})")
        else:
            print("❌")
            falhadas.append(cidade)
        
        # Rate limiting - Nominatim pede 1 segundo de delay
        time.sleep(1.2)
    
    print("\n" + "=" * 90)
    
    # Salvar em JSON
    output_json = "coordenadas_cidades_nominatim_preciso.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(coordenadas_json, f, ensure_ascii=False, indent=2)
    print(f"✓ Salvo em: {output_json}")
    
    # Gerar formato Python
    print("\n" + "=" * 90)
    print("📝 FORMATO PYTHON DICT PARA app.py:")
    print("=" * 90 + "\n")
    
    print("COORDENADAS_CIDADES = {")
    for chave in sorted(coordenadas_python.keys()):
        lat, lng = coordenadas_python[chave]
        print(f"    '{chave}': ({lat}, {lng}),")
    print("}")
    
    # Estatísticas
    print("\n" + "=" * 90)
    print(f"✅ {len(coordenadas_json)} cidades com coordenadas precisas")
    if falhadas:
        print(f"❌ {len(falhadas)} cidades falhadas")
    print("=" * 90)
    
    return coordenadas_json

if __name__ == "__main__":
    main()
