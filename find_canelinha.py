from app import PASTAS_DISPONIVEIS

print('Procurando pastas de Canelinha:')
for chave, info in PASTAS_DISPONIVEIS.items():
    if 'canelinha' in chave.lower() or 'canelinha' in info['cidade'].lower():
        print(f'  Chave: {chave}')
        print(f'    Nome amigável: {info["nome_amigavel"]}')
        print(f'    Caminho: {info["caminho"]}')
