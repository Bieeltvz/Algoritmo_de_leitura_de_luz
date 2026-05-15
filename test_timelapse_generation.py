#!/usr/bin/env python3
"""
Teste gerando timelapse real com o algoritmo corrigido
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento

m = MapaCrescimento()

# Lista de cidades com imagens
cidades_teste = [
    'Bombinhas_recorte',
    'Picarras_recorte'
]

print("=== Gerando timelapse com algoritmo corrigido ===\n")

for cidade in cidades_teste:
    print(f"Processando: {cidade}")
    
    # Procurar pasta da cidade
    pasta_base = Path(__file__).parent.absolute()
    pasta_cidade = None
    
    # Procurar em subpastas
    for item in pasta_base.iterdir():
        if item.is_dir() and cidade.lower() in item.name.lower():
            pasta_cidade = item
            break
    
    if pasta_cidade is None:
        print(f"  ⚠️ Pasta não encontrada para {cidade}")
        continue
    
    # Verificar se tem imagens TIF
    tif_files = list(pasta_cidade.glob('*.tif')) + list(pasta_cidade.glob('VIIRS_*.tif'))
    if not tif_files:
        print(f"  ⚠️ Nenhuma imagem TIF encontrada em {pasta_cidade}")
        continue
    
    print(f"  Encontradas {len(tif_files)} imagens TIF")
    
    # Gerar timelapse
    try:
        arquivo_saida = f"timelapse_{cidade}_corrigido.html"
        resultado = m.gerar_timelapse_cidade(cidade, str(pasta_cidade), arquivo_saida)
        if resultado:
            print(f"  ✅ Timelapse gerado: {arquivo_saida}")
        else:
            print(f"  ❌ Erro ao gerar timelapse")
    except Exception as e:
        print(f"  ❌ Erro: {e}")
    
    print()

print("✅ Teste concluído!")
