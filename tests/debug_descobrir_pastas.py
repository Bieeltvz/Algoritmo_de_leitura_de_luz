#!/usr/bin/env python3
"""
Debug: Verificar nomes de pastas descobertas
"""

from pathlib import Path
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Reproduzir lógica do app.py
CAMINHO_DOCUMENTOS = Path.home() / "Documents"

print("Procurando pastas em:", CAMINHO_DOCUMENTOS)
print()

pastas_braco = {}

try:
    for cidade_dir in CAMINHO_DOCUMENTOS.iterdir():
        if not cidade_dir.is_dir():
            continue
        
        nome_cidade = cidade_dir.name.lower()
        
        # Verifica se contém 'noturno' ou 'noturna'
        if not ('noturno' in nome_cidade or 'noturna' in nome_cidade):
            continue
        
        print(f"Pasta de cidade encontrada: {cidade_dir.name}")
        
        # Dentro procura por "Raster"
        raster_dir = None
        for item in cidade_dir.iterdir():
            if item.is_dir() and item.name.lower() == 'raster':
                raster_dir = item
                break
        
        if not raster_dir:
            print("  ❌ Nenhuma pasta Raster encontrada")
            continue
        
        print(f"  ✅ Pasta Raster encontrada: {raster_dir.name}")
        
        # Dentro de Raster procura por QUALQUER pasta que contenha .tif
        for recorte_dir in raster_dir.iterdir():
            if not recorte_dir.is_dir():
                continue
            
            total_imagens = len(list(recorte_dir.glob('*/*.tif'))) + len(list(recorte_dir.glob('*.tif')))
            
            if total_imagens == 0:
                continue
            
            print(f"    📁 Recorte: {recorte_dir.name} ({total_imagens} imagens)")
            
            # Verificar se é braco
            if 'braco' in recorte_dir.name.lower():
                pastas_braco[recorte_dir.name] = {
                    'caminho': recorte_dir,
                    'total_imagens': total_imagens,
                    'cidade_dir': cidade_dir.name
                }
            
            # Aplicar a lógica de limpeza
            cidade_nome = cidade_dir.name.replace('_noturno', '').replace('_noturna', '').replace('_', ' ').strip()
            
            recorte_nome_original = recorte_dir.name.lower()
            
            if 'reprojet' in recorte_nome_original:
                recorte_tipo = 'Reprojetados'
            else:
                # Remover sufixos e manter o nome específico
                # IMPORTANTE: Remover '_recortes' ANTES de '_recorte' para evitar deixar 's' solto
                recorte_tipo = recorte_dir.name.replace('_recortes', '').replace('_recorte', '').replace('_recortado', '').replace('_', ' ').strip()
                print(f"        DEBUG 1 - After prefix removal: '{recorte_tipo}'")
                
                # Remover palavras-chave que possam ter ficado soltas
                for palavra in ['recortes', 'recorte', 'recortado', 'reprojet']:
                    recorte_tipo = recorte_tipo.replace(palavra, '').strip()
                recorte_tipo = ' '.join(recorte_tipo.split())  # Limpar espaços múltiplos
                print(f"        DEBUG 2 - After word removal: '{recorte_tipo}'")
                
                if not recorte_tipo or recorte_tipo.lower() == cidade_nome.lower():
                    recorte_tipo = recorte_dir.name.replace('_', ' ').strip()
                    # Remover sufixos comuns também dessa segunda passagem
                    for palavra in ['recortes', 'recorte', 'recortado', 'reprojet', 'noturno', 'noturna']:
                        recorte_tipo = recorte_tipo.replace(palavra, '').strip()
                    recorte_tipo = ' '.join(recorte_tipo.split())  # Limpar espaços múltiplos
                    print(f"        DEBUG 3 - Using full name with cleaning: '{recorte_tipo}'")
                
                if not recorte_tipo:
                    recorte_tipo = 'Recorte'
                    print(f"        DEBUG 4 - Using default: '{recorte_tipo}'")
            
            cidade_nome = cidade_nome.title()
            recorte_tipo = recorte_tipo.title()
            
            nome_amigavel = f"{cidade_nome} - {recorte_tipo}".strip()
            
            print(f"      Processado:")
            print(f"        Nome cidade: {cidade_nome}")
            print(f"        Tipo recorte: {recorte_tipo}")
            print(f"        Nome amigável: {nome_amigavel}")
            print()

except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()

print("=" * 70)
print("PASTAS COM 'BRACO' ENCONTRADAS:")
print("=" * 70)
for nome, info in pastas_braco.items():
    print(f"  {nome}")
    print(f"    Cidade: {info['cidade_dir']}")
    print(f"    Imagens: {info['total_imagens']}")
