#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
from pathlib import Path
os.chdir(Path(__file__).parent)
sys.path.insert(0, '.')

print("Iniciando processamento...")
from processador_paralelo import ProcessadorParalelo

pasta = Path(r'C:\Users\gtvargas\Documents\balneario_camboriu_noturno\RASTER\picarras_recortado')
print(f'Pasta: {pasta.exists()}')

p = ProcessadorParalelo(nome_cidade='picarras_recortado', workers=3)
p.processar_pasta(pasta)
print('FIM')
