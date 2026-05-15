#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()))

from processador_paralelo import ProcessadorParalelo

# Configurar a pasta
pasta_raster = Path.home() / 'Documents' / 'Barra_Velha_Noturna' / 'Raster' / 'REPROJETADOS'

print(f"📁 Processando: {pasta_raster}")
print(f"📊 Buscando arquivos .tif...")

# Buscar TIFFs
tifs = sorted(pasta_raster.rglob('*.tif'))
print(f"✅ Encontrado {len(tifs)} arquivos TIFF")

if not tifs:
    print("❌ Nenhum arquivo TIFF encontrado!")
    sys.exit(1)

# Processar
processador = ProcessadorParalelo(numero_workers=4)
print(f"⚙️  Iniciando processamento com 4 workers...")
resultados = processador.processar_pasta(str(pasta_raster))

# Salvar CSV
arquivo_csv = 'resultados_Barra_Velha_Noturna.csv'
print(f"\n💾 Salvando em: {arquivo_csv}")
processador.salvar_csv(arquivo_csv, resultados)

print(f"✅ Concluído! {len(resultados)} registros salvos.")
