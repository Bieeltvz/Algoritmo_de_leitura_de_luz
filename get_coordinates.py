import requests
import json
import time
import unicodedata

# List of cities in Santa Catarina, Brazil
cities = [
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

def remove_accents(text):
    """Remove accents from text and convert to lowercase"""
    nfd_form = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd_form if unicodedata.category(char) != 'Mn').lower()

def get_coordinates(city_name):
    """Get coordinates from Nominatim API"""
    try:
        query = f"{city_name}, Santa Catarina, Brazil"
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data:
            result = data[0]
            lat = float(result['lat'])
            lng = float(result['lon'])
            return (lat, lng)
        else:
            print(f"No results for {city_name}")
            return None
    except Exception as e:
        print(f"Error fetching coordinates for {city_name}: {e}")
        return None

# Fetch coordinates
coordinates_dict = {}

print("Fetching coordinates from Nominatim/OpenStreetMap...")
print(f"Processing {len(cities)} cities...\n")

for i, city in enumerate(cities, 1):
    coords = get_coordinates(city)
    if coords:
        key = remove_accents(city)
        coordinates_dict[key] = coords
        print(f"[{i}/{len(cities)}] {city}: {coords}")
    else:
        print(f"[{i}/{len(cities)}] {city}: FAILED")
    
    # Rate limiting - Nominatim requests 1 second delay between requests
    time.sleep(1.1)

# Save to JSON file
with open("coordenadas_cidades_completas_nominatim.json", "w", encoding="utf-8") as f:
    json.dump(coordinates_dict, f, ensure_ascii=False, indent=2)

# Print Python dict format
print("\n" + "="*80)
print("COORDINATES IN PYTHON DICT FORMAT:")
print("="*80 + "\n")
print("coordinates = {")
for key in sorted(coordinates_dict.keys()):
    lat, lng = coordinates_dict[key]
    print(f'    "{key}": ({lat}, {lng}),')
print("}")

print(f"\n✓ Successfully retrieved {len(coordinates_dict)} coordinates")
print(f"✓ Saved to: coordenadas_cidades_completas_nominatim.json")
