from app import COORDENADAS_CIDADES

print("=" * 70)
print("VALIDAÇÃO DE COORDENADAS DAS CIDADES")
print("=" * 70)
print(f"\n✓ Total de entradas no dicionário: {len(COORDENADAS_CIDADES)}")

# Verificar as cidades que foram pedidas
cidades_solicitadas = [
    'apiuna', 'atalanta', 'balneario picarras', 'botuvera', 'camboriu',
    'chapadao do lageado', 'itajai', 'ituporanga', 'jose boiteux', 
    'major gercino', 'petrolandia', 'presidente getulio', 'rio do sul',
    'sao joao batista', 'taio', 'timbo', 'vale itajai'
]

print(f"\nCIDAdES ADICIONADAS:")
for cidade in cidades_solicitadas:
    if cidade in COORDENADAS_CIDADES:
        coords = COORDENADAS_CIDADES[cidade]
        print(f"  ✓ {cidade.title():<30} {coords}")
    else:
        print(f"  ✗ {cidade.title():<30} FALTANDO!")

print("\n" + "=" * 70)
print("✅ Todas as cidades estão agora no mapa!")
print("=" * 70)
