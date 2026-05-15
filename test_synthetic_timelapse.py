#!/usr/bin/env python3
"""
Teste do timelapse com imagens sintéticas para validar a funcionalidade de overlay de cores
"""

import numpy as np
from PIL import Image
from pathlib import Path
import rasterio
from rasterio.transform import from_bounds
import tempfile
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Criar pasta temporária para imagens de teste
test_dir = Path("Bombinhas_recorte_test")
test_dir.mkdir(exist_ok=True)

logger.info(f"Criando imagens sintéticas em {test_dir}...")

# Gerar 12 imagens de crescimento progressivo
for ano_idx in range(12):
    # Criar imagem com padrão de crescimento
    img = np.random.randint(50, 150, size=(512, 512), dtype=np.uint8)
    
    # Adicionar área de crescimento (aumenta com o tempo)
    growth_mask = np.zeros((512, 512), dtype=np.uint8)
    growth_size = int(50 + ano_idx * 15)  # Cresce ao longo do tempo
    growth_mask[100:100+growth_size, 100:100+growth_size] = 30 + ano_idx * 5
    
    img = img + growth_mask
    
    # Salvar como GeoTIFF
    img_path = test_dir / f"VIIRS_{ano_idx:02d}.tif"
    
    with rasterio.open(
        img_path,
        'w',
        driver='GTiff',
        height=512,
        width=512,
        count=1,
        dtype=rasterio.float32,
        transform=from_bounds(0, 0, 512, 512, 512, 512),
    ) as dst:
        dst.write(img, 1)
    
    logger.info(f"✅ Criada {img_path.name}")

logger.info(f"\n📊 Gerando timelapse com imagens sintéticas...")

from mapa_crescimento import MapaCrescimento

mapa = MapaCrescimento()
mapa.carregar_coordenadas()

html_output = "test_timelapse_synthetic.html"

# Tentar gerar timelapse
try:
    resultado = mapa.gerar_timelapse_cidade(
        "Bombinhas_recorte_test",
        str(test_dir),
        html_output
    )
    
    if resultado:
        logger.info(f"✅ Timelapse gerado com sucesso: {html_output}")
        logger.info(f"📋 Verifique o arquivo: {Path(html_output).absolute()}")
    else:
        logger.error("❌ Falha ao gerar timelapse")
        
except Exception as e:
    logger.error(f"❌ Erro: {e}", exc_info=True)

# Limpeza
logger.info(f"\n🧹 Removendo imagens de teste...")
import shutil
shutil.rmtree(test_dir)
logger.info("Concluído!")
