#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script que simula a descoberta automática de cidades (exatamente como app.py faz)
"""

from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CAMINHO_DOCUMENTOS = Path(r"C:\Users\gtvargas\Documents")

def descobrir_pastas_cidades():
    """
    Descobre automaticamente todas as cidades e suas pastas de recorte
    Procura por padrão muito flexível:
    - Documents/*noturno* ou *noturna* → Raster/RASTER → Qualquer pasta com .tif
    """
    pastas_encontradas = {}
    
    if not CAMINHO_DOCUMENTOS.exists():
        logger.warning(f"Documentos não encontrado: {CAMINHO_DOCUMENTOS}")
        return pastas_encontradas
    
    try:
        # Procura pastas com padrão "*noturno*" ou "*noturna*"
        for cidade_dir in CAMINHO_DOCUMENTOS.iterdir():
            if not cidade_dir.is_dir():
                continue
            
            nome_cidade = cidade_dir.name.lower()
            # Verifica se contém 'noturno' ou 'noturna'
            if not ('noturno' in nome_cidade or 'noturna' in nome_cidade):
                continue
            
            # Dentro procura por "Raster" ou "RASTER" (case-insensitive)
            raster_dir = None
            for item in cidade_dir.iterdir():
                if item.is_dir() and item.name.lower() == 'raster':
                    raster_dir = item
                    break
            
            if not raster_dir:
                continue
            
            # Dentro de Raster procura por QUALQUER pasta que contenha .tif
            for recorte_dir in raster_dir.iterdir():
                if not recorte_dir.is_dir():
                    continue
                
                # Contar imagens nesta pasta (procura recursivamente)
                total_imagens = len(list(recorte_dir.glob('*/*.tif'))) + len(list(recorte_dir.glob('*.tif')))
                
                # Se não tem imagens, pula
                if total_imagens == 0:
                    continue
                
                # Extrair nome amigável
                # Remove "_noturno", "_noturna" e formata
                cidade_nome = cidade_dir.name.replace('_noturno', '').replace('_noturna', '').replace('_', ' ').strip()
                
                # Remove possíveis sufixos de recorte: "_recorte", "_recortes", "_recortado", etc
                recorte_tipo = recorte_dir.name.replace('_recorte', '').replace('_recortes', '').replace('_recortado', '').replace('_', ' ').strip()
                
                # Se recorte_tipo for vazio ou igual à cidade, usa "Recorte" como padrão
                if not recorte_tipo or recorte_tipo.lower() == cidade_nome.lower():
                    recorte_tipo = 'Recorte'
                
                # Formatar com title case
                cidade_nome = cidade_nome.title()
                recorte_tipo = recorte_tipo.title()
                
                chave = f"{recorte_dir.name}"
                nome_amigavel = f"{cidade_nome} - {recorte_tipo}".strip()
                
                pastas_encontradas[chave] = {
                    'caminho': recorte_dir,
                    'nome': recorte_dir.name,
                    'cidade': cidade_nome,
                    'tipo_recorte': recorte_tipo,
                    'nome_amigavel': nome_amigavel,
                    'total_imagens': total_imagens,
                    'cidade_dir': cidade_dir
                }
                
                logger.info(f"Cidade encontrada: {nome_amigavel} ({total_imagens} imagens)")
    except Exception as e:
        logger.error(f"Erro ao descobrir pastas: {e}")
    
    return pastas_encontradas

print("=" * 100)
print("SIMULANDO DESCOBERTA AUTOMÁTICA (app.py)")
print("=" * 100)

pastas = descobrir_pastas_cidades()

print(f"\nTotal de pastas descobertas: {len(pastas)}")
print("\n" + "=" * 100)
print("PASTAS ENCONTRADAS:")
print("=" * 100)

for i, (chave, info) in enumerate(sorted(pastas.items()), 1):
    print(f"\n{i}. {info['nome_amigavel']}")
    print(f"   Chave: {chave}")
    print(f"   Caminho: {info['caminho']}")
    print(f"   Imagens: {info['total_imagens']}")

# Procurar especificamente por Balneário
print("\n" + "=" * 100)
print("PROCURANDO BALNEÁRIO:")
print("=" * 100)

balneario_encontradas = [info for info in pastas.values() if 'balneario' in info['cidade'].lower() or 'picarras' in info['cidade'].lower()]

if balneario_encontradas:
    print(f"\n✓ Encontradas {len(balneario_encontradas)} entradas com 'Balneário' ou 'Picarras':")
    for info in balneario_encontradas:
        print(f"  - {info['nome_amigavel']}")
else:
    print("\n✗ NENHUMA entrada com 'Balneário' ou 'Picarras' encontrada!")
