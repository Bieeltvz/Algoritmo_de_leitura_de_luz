#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reprocessa a pasta do Balneário Camboriú com a correção de parsing de filename
"""

import sys
from pathlib import Path

DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
sys.path.insert(0, str(DIRETORIO_TRABALHO))

from processador_paralelo import ProcessadorParalelo

# Caminho correto do Balneário Camboriú
pasta_balneario = Path("C:\\Users\\gtvargas\\Documents\\balneario_camboriu_noturno\\RASTER\\picarras_recortado")

print("\n" + "=" * 100)
print("REPROCESSANDO BALNEÁRIO CAMBORIÚ COM CORREÇÃO DE PARSING")
print("=" * 100)
print(f"Pasta: {pasta_balneario}")
print(f"Verificando se existe...")

if not pasta_balneario.exists():
    print(f"ERRO: Pasta não encontrada: {pasta_balneario}")
    sys.exit(1)

# Contar imagens
imagens = list(pasta_balneario.glob('**/*.tif'))
print(f"Total de imagens: {len(imagens)}")

print("\n" + "=" * 100)
print("INICIANDO PROCESSAMENTO")
print("=" * 100)

# Processar com o nome correto
processador = ProcessadorParalelo(
    workers=4,
    nome_cidade='picarras_recortado',
    diretorio_trabalho=str(DIRETORIO_TRABALHO),
    forcar_reprocessamento=True  # Force reprocessar
)

processador.processar_pasta(pasta_balneario)

print("\n" + "=" * 100)
print("PROCESSAMENTO CONCLUÍDO!")
print("=" * 100)
