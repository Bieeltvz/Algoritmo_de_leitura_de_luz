#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reprocessa o Balneário Camboriú com retry de erros
"""

import sys
from pathlib import Path
import json

DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
sys.path.insert(0, str(DIRETORIO_TRABALHO))

from processador_paralelo import ProcessadorParalelo

pasta_balneario = Path("C:\\Users\\gtvargas\\Documents\\balneario_camboriu_noturno\\RASTER\\picarras_recortado")

print("\n" + "=" * 100)
print("REPROCESSANDO BALNEÁRIO CAMBORIÚ")
print("=" * 100)

if not pasta_balneario.exists():
    print(f"ERRO: Pasta não encontrada!")
    sys.exit(1)

# Limpar cache anterior
cache_file = DIRETORIO_TRABALHO / 'processados_picarras_recortado.json'
if cache_file.exists():
    cache_file.unlink()
    print(f"Cache limpo: {cache_file.name}")

# Criar processador
processador = ProcessadorParalelo(
    workers=4,
    nome_cidade='picarras_recortado',
    diretorio_trabalho=str(DIRETORIO_TRABALHO)
)

# Processar
print(f"\nProcessando {len(list(pasta_balneario.glob('**/*.tif')))} imagens...")
processador.processar_pasta(pasta_balneario)

print("\nConcluído!")
