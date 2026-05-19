#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para processar TODAS as cidades descobertas em paralelo
Solução para o problema de "continua nao aparecendo o resultado em varias cidades"
"""

import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup
DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
os.chdir(DIRETORIO_TRABALHO)
sys.path.insert(0, str(DIRETORIO_TRABALHO))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from app import descobrir_pastas_cidades
from processador_paralelo import ProcessadorParalelo

def processar_uma_cidade(chave, info):
    """Processa uma única cidade"""
    nome_cidade = info['nome']
    nome_amigavel = info['nome_amigavel']
    caminho = info['caminho']
    
    # Verificar se já tem resultado
    arquivo_resultado = DIRETORIO_TRABALHO / f'resultados_{nome_cidade}.csv'
    if arquivo_resultado.exists():
        linhas = sum(1 for _ in open(arquivo_resultado)) - 1  # Subtrair header
        logger.info(f"[SKIP] PULANDO: {nome_amigavel} (já tem {linhas} resultados)")
        return True
    
    try:
        logger.info(f"[PROCESSANDO] {nome_amigavel} ({caminho})")
        
        # Criar processador para esta cidade
        processador = ProcessadorParalelo(
            workers=4,
            nome_cidade=nome_cidade,
            diretorio_trabalho=str(DIRETORIO_TRABALHO)
        )
        
        # Processar a pasta
        processador.processar_pasta(caminho)
        
        logger.info(f"[OK] SUCESSO: {nome_amigavel}")
        return True
        
    except Exception as e:
        logger.error(f"[ERRO] ERRO em {nome_amigavel}: {e}")
        return False


def main():
    """Processa todas as cidades"""
    
    print("\n" + "=" * 100)
    print("DESCOBRINDO CIDADES...")
    print("=" * 100)
    
    pastas = descobrir_pastas_cidades()
    
    print("\n" + "=" * 100)
    print(f"ENCONTRADAS: {len(pastas)} CIDADES")
    print("=" * 100)
    
    # Separar cidades com e sem resultado
    cidades_com_resultado = []
    cidades_sem_resultado = []
    
    for chave, info in sorted(pastas.items()):
        arquivo_resultado = DIRETORIO_TRABALHO / f'resultados_{info["nome"]}.csv'
        if arquivo_resultado.exists():
            linhas = sum(1 for _ in open(arquivo_resultado)) - 1
            cidades_com_resultado.append((info['nome_amigavel'], linhas))
        else:
            cidades_sem_resultado.append((chave, info))
    
    print(f"\nCOM RESULTADOS: {len(cidades_com_resultado)}")
    for nome, linhas in sorted(cidades_com_resultado):
        print(f"   {nome} ({linhas} linhas)")
    
    print(f"\nSEM RESULTADOS: {len(cidades_sem_resultado)}")
    for chave, info in cidades_sem_resultado[:10]:  # Mostrar primeiras 10
        print(f"   {info['nome_amigavel']}")
    if len(cidades_sem_resultado) > 10:
        print(f"   ... e mais {len(cidades_sem_resultado) - 10}")
    
    if len(cidades_sem_resultado) == 0:
        print("\nTODAS AS CIDADES JÁ TÊM RESULTADOS!")
        return
    
    # Processar em paralelo (máximo 2 simultâneas para não sobrecarregar)
    print("\n" + "=" * 100)
    print(f"INICIANDO PROCESSAMENTO DE {len(cidades_sem_resultado)} CIDADES...")
    print("=" * 100)
    
    processadas = 0
    erros = 0
    tempo_inicio = time.time()
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {}
        for chave, info in cidades_sem_resultado:
            future = executor.submit(processar_uma_cidade, chave, info)
            futures[future] = info['nome_amigavel']
        
        for future in as_completed(futures):
            nome = futures[future]
            try:
                if future.result():
                    processadas += 1
                else:
                    erros += 1
            except Exception as e:
                logger.error(f"[ERRO] ERRO ao processar {nome}: {e}")
                erros += 1
    
    tempo_total = time.time() - tempo_inicio
    
    print("\n" + "=" * 100)
    print("RESUMO DO PROCESSAMENTO")
    print("=" * 100)
    print(f"Processadas com sucesso: {processadas}/{len(cidades_sem_resultado)}")
    print(f"Erros: {erros}")
    print(f"Tempo total: {tempo_total:.1f}s ({tempo_total/60:.1f}min)")
    print("=" * 100 + "\n")


if __name__ == '__main__':
    main()
