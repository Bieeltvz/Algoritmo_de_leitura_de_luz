#!/usr/bin/env python3
"""
Debug string cleaning logic
"""

nome = "Braco_Do_Trombudo_recortes"

print(f"Original: {nome}")

# Step 1
result = nome.replace('_recortes', '').replace('_recorte', '').replace('_recortado', '')
print(f"After replace prefixes: {result}")

# Step 2
result = result.replace('_', ' ').strip()
print(f"After replace underscore: {result}")

# Step 3
for palavra in ['recortes', 'recorte', 'recortado', 'reprojet']:
    result = result.replace(palavra, '').strip()
    print(f"  After remove '{palavra}': {result}")

result = ' '.join(result.split())
print(f"After clean spaces: {result}")

print()
print("Expected: Braco Do Trombudo")
