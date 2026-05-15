import json
import requests

# Try alternative search terms for the missing cities
missing_cities = ["Guide", "Ituparanga"]

def get_coordinates(city_name, alternative_search=None):
    """Try to get coordinates with alternative search"""
    try:
        search_terms = [city_name]
        if alternative_search:
            search_terms.append(alternative_search)
        
        for search_term in search_terms:
            query = f"{search_term}, Santa Catarina, Brazil"
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
                print(f"✓ {city_name}: ({lat}, {lng})")
                return (lat, lng)
            
            import time
            time.sleep(1.1)
        
        return None
    except Exception as e:
        print(f"✗ {city_name}: {e}")
        return None

# Try to find the missing cities
print("Attempting to locate missing cities...\n")

# Guide might be "Guia" or search with different terms
guide_coords = get_coordinates("Guide")
if not guide_coords:
    # Try alternative spellings
    guide_coords = get_coordinates("Guia dos Imigrantes", "Guia")

# Ituparanga might be spelled differently
ituparanga_coords = get_coordinates("Ituparanga")
if not ituparanga_coords:
    ituparanga_coords = get_coordinates("Ituparanga, Rio do Oeste")

print("\n" + "="*60)
print("RESULTS FOR MISSING CITIES:")
print("="*60)

if guide_coords:
    print(f'"guide": {guide_coords},')
else:
    print('"guide": NOT FOUND - City may not exist or have different name')

if ituparanga_coords:
    print(f'"ituparanga": {ituparanga_coords},')
else:
    print('"ituparanga": NOT FOUND - City may not exist or have different name')
