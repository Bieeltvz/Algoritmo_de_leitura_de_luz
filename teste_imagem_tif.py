"""
Script para testar o algoritmo com a imagem TIFF de Bombinhas
SEM redimensionar para 500x500
"""

import numpy as np
from pathlib import Path
from leitura_de_luz import AnalisadorLuzSatelite
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho da imagem TIFF fornecida
CAMINHO_IMAGEM = r"C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Bombinhas_recorte\2014\Bombinhas_2014_01.tif"

def testar_imagem_tif():
    """Testa o algoritmo com a imagem TIFF de Bombinhas - DIMENSÕES ORIGINAIS"""
    
    # Validar existência do arquivo
    caminho = Path(CAMINHO_IMAGEM)
    if not caminho.exists():
        logger.error(f"❌ Arquivo não encontrado: {CAMINHO_IMAGEM}")
        return False
    
    logger.info(f"📂 Carregando imagem: {caminho.name}")
    logger.info(f"   Tamanho do arquivo: {caminho.stat().st_size / 1024:.2f} KB")
    
    try:
        # Carregar com rasterio
        import rasterio
        with rasterio.open(caminho) as src:
            imagem = src.read()
            # Se multicamada, pegar a primeira
            if len(imagem.shape) > 2:
                logger.info(f"   Imagem multicamada ({imagem.shape[0]} canais), usando primeiro canal")
                imagem = imagem[0]
            imagem = np.array(imagem, dtype=float)
        
        logger.info(f"✅ Imagem carregada com sucesso!")
        logger.info(f"   Dimensões originais: {imagem.shape}")
        logger.info(f"   Tipo de dados: {imagem.dtype}")
        logger.info(f"   Valor mínimo (original): {np.min(imagem):.2f}")
        logger.info(f"   Valor máximo (original): {np.max(imagem):.2f}")
        logger.info(f"   Valor médio (original): {np.nanmean(imagem):.2f}")
        
        # NÃO converter -9999 para NaN - deixar para o algoritmo detectar em modo geoespacial
        # O algoritmo inteligente vai diferenciar NoData (-9999) de erros reais
        
        # NÃO converter -9999 para NaN - deixar para o algoritmo detectar em modo geoespacial
        # O algoritmo inteligente vai diferenciar NoData (-9999) de erros reais
        
        # Normalizar para 0-255 se necessário
        min_val = np.min(imagem)
        max_val = np.max(imagem)
        
        if min_val >= 0 and max_val <= 255:
            logger.info(f"   ℹ️ Imagem já está em escala 0-255")
        elif max_val > 255:
            logger.info(f"   ℹ️ Normalizando imagem de [{min_val:.0f}, {max_val:.0f}] para [0, 255]")
            # Normalizar mantendo -9999 como está (para o algoritmo detectar)
            mascara_nodata = imagem == -9999
            imagem_temp = imagem.copy()
            imagem_temp[mascara_nodata] = 0  # Temporariamente substituir para cálculo
            
            min_val_real = np.min(imagem_temp[~mascara_nodata]) if np.sum(~mascara_nodata) > 0 else 0
            max_val_real = np.max(imagem_temp[~mascara_nodata]) if np.sum(~mascara_nodata) > 0 else 255
            
            imagem[~mascara_nodata] = 255 * (imagem_temp[~mascara_nodata] - min_val_real) / (max_val_real - min_val_real + 1e-10)
            imagem[~mascara_nodata] = np.clip(imagem[~mascara_nodata], 0, 255)
        
        logger.info(f"✅ Dimensões MANTIDAS: {imagem.shape}")
        logger.info(f"   Valor médio (processado): {np.nanmean(imagem):.2f}")
        
        # Criar analisador COM MODO GEOESPACIAL
        logger.info("\n📊 Iniciando análise com o algoritmo (MODO GEOESPACIAL)...")
        analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0, modo_geoespacial=True)
        
        # Temporariamente alterar tamanho esperado
        tamanho_original = analisador.TAMANHO_ESPERADO
        analisador.TAMANHO_ESPERADO = imagem.shape
        
        logger.info(f"   Tamanho esperado: {analisador.TAMANHO_ESPERADO}")
        
        # Processar imagem
        stats = analisador.processar_imagem(imagem)
        
        # Restaurar tamanho original
        analisador.TAMANHO_ESPERADO = tamanho_original
        
        # Gerar e exibir relatório
        relatorio = analisador.gerar_relatorio(stats)
        print("\n" + "="*70)
        print(relatorio)
        print("="*70)
        
        # Informações adicionais
        logger.info("\n📈 Análise Detalhada:")
        logger.info(f"   Total de pixels: {stats.total_pixels:,}")
        logger.info(f"   Pixels válidos: {stats.pixels_validos:,} ({stats.percentual_valido:.1f}%)")
        logger.info(f"   Pixels nulos: {stats.pixels_nulos:,}")
        logger.info(f"   Pixels outliers: {stats.pixels_outliers:,}")
        logger.info(f"   Threshold para outliers: {stats.threshold_outlier:.2f}")
        logger.info(f"   Intensidade média: {stats.intensidade_media:.2f}")
        logger.info(f"   Intensidade mediana: {stats.intensidade_mediana:.2f}")
        logger.info(f"   Desvio padrão: {stats.desvio_padrao:.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar imagem: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🚀 TESTE DO ALGORITMO COM IMAGEM TIFF (SEM REDIMENSIONAMENTO)")
    print("="*70)
    sucesso = testar_imagem_tif()
    print("="*70)
    if sucesso:
        print("\n✅ Teste concluído com sucesso!")
    else:
        print("\n❌ Teste falhou!")
        sys.exit(1)
