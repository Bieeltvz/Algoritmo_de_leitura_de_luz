#!/usr/bin/env python3
"""
Debug coordinate name matching in mapa_crescimento.py
"""

nome_cidade = "Braco_Do_Trombudo_recortes"

print(f"Input: {nome_cidade}")

# Step 1: Replace underscores
nome_exibicao = nome_cidade.replace('_', ' ')
print(f"After replacing underscores: '{nome_exibicao}'")

# Step 2: lowercase and remove suffixes
nome_busca = nome_exibicao.lower()
print(f"After lowercase: '{nome_busca}'")
print(f"  Chars: {[c for c in nome_busca]}")

print("\nRemoving suffixes:")
for sufixo in ['recortes', 'recorte', 'recortado', 'reprojetado', 'reprojet', 'noturno', 'noturna']:
    novo_nome_1 = nome_busca.replace(f' {sufixo}', '')
    novo_nome_2 = novo_nome_1.replace(f'_{sufixo}', '')
    if novo_nome_2 != nome_busca:
        print(f"  {sufixo}:")
        print(f"    After replace ' {sufixo}': '{novo_nome_1}'")
        print(f"    After replace _{sufixo}: '{novo_nome_2}'")
        nome_busca = novo_nome_2
    else:
        print(f"  {sufixo}: (no change)")

print(f"\nFinal nome_busca: '{nome_busca}'")
print(f"  Chars: {[c for c in nome_busca]}")

print("\nExpected: 'braco do trombudo'")
print(f"Got: '{nome_busca}'")
print(f"Match: {nome_busca == 'braco do trombudo'}")

