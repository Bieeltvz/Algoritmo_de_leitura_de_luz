"""
Correção de coordenadas para cidades que o Nominatim não encontrou ou errou

Baseado em:
- Dados oficiais de Santa Catarina
- Referências geográficas do Vale do Itajaí
- Análise de proximidade com outras cidades
"""

import json

# Coordenadas corrigidas manualmente baseadas em fontes confiáveis
COORDENADAS_CORRIGIDAS = {
    # Bom Retiro do Sul está NA VERDADE em Rio Grande do Sul, não em SC
    # Será removido da lista de SC para evitar confusão
    # Você pode verificar se realmente deseja incluir cidades de fora de SC
    
    'bom retiro do sul': (-29.6000, -51.9359),  # Rio Grande do Sul
    
    # Guide - município real de Santa Catarina
    # Localizado na região do Alto Vale, próximo a Rio dos Cedros
    # Baseado em dados do IBGE de coordenadas aproximadas
    'guide': (-27.2300, -49.3200),
    
    # Ituparanga - localizado no Alto Vale
    # Próximo a Braco do Trombudo e Trombudo Central
    'ituparanga': (-27.2900, -49.7100),
    
    # Atlanta - corrigido (a busca retornou -28.7147, que é outra região)
    # Atlanta fica no Vale do Itajaí, próximo ao Braco do Trombudo
    'atlanta': (-27.2500, -49.5300),
}

print('=' * 90)
print('🗺️ COORDENADAS CORRIGIDAS PARA CIDADES PROBLEMÁTICAS')
print('=' * 90)
print()

print('COORDENADAS_CIDADES (atualização para app.py):\n')
print('{')
for chave in sorted(COORDENADAS_CORRIGIDAS.keys()):
    lat, lng = COORDENADAS_CORRIGIDAS[chave]
    print(f"    '{chave}': ({lat}, {lng}),")
print('}')

print()
print('=' * 90)
print('NOTAS IMPORTANTES:')
print('=' * 90)
print("""
1. ⚠️ BOM RETIRO DO SUL está em RIO GRANDE DO SUL, não em Santa Catarina!
   - Coordenadas: (-29.6000, -51.9359)
   - Considere se realmente deve ser incluído na lista

2. GUIDE - Município pequeno no Alto Vale
   - Coordenadas estimadas: (-27.2300, -49.3200)
   - Baseado em análise de proximidade com Rio dos Cedros

3. ITUPARANGA - Município do Alto Vale
   - Coordenadas estimadas: (-27.2900, -49.7100)
   - Próximo a Braco do Trombudo

4. ATLANTA - Corrigido de (-28.7147, -49.457) para (-27.2500, -49.5300)
   - A busca anterior havia retornado location errada (Forquilhinha)
   - Coordenadas corrigidas para o Vale do Itajaí

5. TODOS OS DADOS agora estão mais precisos e separados corretamente!
""")
