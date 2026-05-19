from app import PASTAS_DISPONIVEIS, PASTA_SELECIONADA

print('PASTA SELECIONADA ATUAL:')
print(f'  Nome: {PASTA_SELECIONADA["nome"]}')

print('\nPROCURANDO CANELINHA:')
for chave, info in PASTAS_DISPONIVEIS.items():
    if 'canelinha' in info['cidade'].lower():
        print(f'  ✓ {chave}: {info["nome_amigavel"]} ({info["cidade"]})')
