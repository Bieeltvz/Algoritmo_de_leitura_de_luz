#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testa se a extração de ano/mês está funcionando corretamente
"""

from pathlib import Path

# Testar com diferentes nomes de arquivo
arquivos_teste = [
    "balneario_camboriu_2014_02.tif",
    "bombinhas_2018_01.tif",
    "rio_dos_cedros_2023_06.tif",
    "picarras_2017_12.tif"
]

print("\n" + "=" * 100)
print("TESTANDO EXTRAÇÃO DE ANO E MÊS")
print("=" * 100)

for nome_arquivo in arquivos_teste:
    path = Path(nome_arquivo)
    partes = path.stem.split('_')
    
    ano = partes[-2] if len(partes) > 1 else '0'
    mes = partes[-1] if len(partes) > 0 else '0'
    
    print(f"\nArquivo: {nome_arquivo}")
    print(f"  Stem: {path.stem}")
    print(f"  Partes: {partes}")
    print(f"  Ano (partes[-2]): {ano}")
    print(f"  Mês (partes[-1]): {mes}")
    
    # Tentar converter para int
    try:
        ano_int = int(ano)
        mes_int = int(mes)
        print(f"  SUCESSO: {ano_int}/{mes_int:02d}")
    except ValueError as e:
        print(f"  ERRO: {e}")

print("\n" + "=" * 100)
