"""
Script para diagnosticar por que a média está tão baixa
Mostra: tipo de dado, valores brutos, distribuição
"""

import numpy as np
import rasterio
from pathlib import Path
import json

def diagnosticar_tiff(caminho_arquivo):
    """Analisa completamente um arquivo TIFF"""
    
    caminho = Path(caminho_arquivo)
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {caminho}")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 DIAGNÓSTICO DO TIFF: {caminho.name}")
    print(f"{'='*60}\n")
    
    with rasterio.open(caminho) as src:
        # Info do arquivo
        print(f"📋 Informações do arquivo TIFF:")
        print(f"  - Driver: {src.driver}")
        print(f"  - Tipo de dado (dtype): {src.dtypes[0]}")  # ← TIPO DE DADO
        print(f"  - Dimensões: {src.shape}")
        print(f"  - Canais: {src.count}")
        print(f"  - NoData value: {src.nodata}")
        print()
        
        # Ler dados
        dados_brutos = src.read(1)  # Ler primeira camada em tipo original
        dados_float = dados_brutos.astype(float)
        
        print(f"📈 Dados BRUTOS (tipo original: {dados_brutos.dtype}):")
        print(f"  - Mínimo: {np.min(dados_brutos)}")
        print(f"  - Máximo: {np.max(dados_brutos)}")
        print(f"  - Média: {np.mean(dados_brutos):.6f}")
        print(f"  - Mediana: {np.median(dados_brutos):.6f}")
        print()
        
        print(f"📊 Dados em FLOAT:")
        print(f"  - Mínimo: {np.min(dados_float):.6f}")
        print(f"  - Máximo: {np.max(dados_float):.6f}")
        print(f"  - Média: {np.mean(dados_float):.6f}")
        print(f"  - Mediana: {np.median(dados_float):.6f}")
        print()
        
        # Distribuição
        print(f"📍 Distribuição de valores:")
        unicos, contagens = np.unique(dados_brutos, return_counts=True)
        print(f"  - Valores únicos: {len(unicos)}")
        
        # Top 10 valores mais frequentes
        top_indices = np.argsort(-contagens)[:10]
        for i, idx in enumerate(top_indices, 1):
            valor = unicos[idx]
            freq = contagens[idx]
            percentual = 100 * freq / dados_brutos.size
            print(f"    {i}. Valor {valor}: {freq:,} pixels ({percentual:.2f}%)")
        print()
        
        # Verificar NoData
        print(f"🔍 Análise de NoData:")
        mascara_nodata = dados_brutos == src.nodata if src.nodata is not None else np.zeros_like(dados_brutos, dtype=bool)
        print(f"  - NoData esperado: {src.nodata}")
        print(f"  - Pixels com -9999: {np.sum(dados_brutos == -9999)}")
        print(f"  - Pixels com 0: {np.sum(dados_brutos == 0)}")
        print(f"  - Total pixels NoData/vazios: {np.sum(mascara_nodata)}")
        print()
        
        # Pixels válidos (removendo NoData)
        dados_validos = dados_float[~mascara_nodata]
        if len(dados_validos) > 0:
            print(f"✅ Sem NoData/zeros (apenas pixels válidos):")
            print(f"  - Quantidade: {len(dados_validos)}")
            print(f"  - Mínimo: {np.min(dados_validos):.6f}")
            print(f"  - Máximo: {np.max(dados_validos):.6f}")
            print(f"  - Média: {np.mean(dados_validos):.6f}")
            print(f"  - Mediana: {np.median(dados_validos):.6f}")
        print()

# Procurar arquivos TIFF de Canelinha automaticamente
if __name__ == "__main__":
    docs = Path(r"C:\Users\gtvargas\Documents")
    
    # Procurar por arquivos TIFF em pastas de cidades
    tiff_files = list(docs.glob("**/Canelinha*/**/*.tif"))
    
    if tiff_files:
        print(f"\n✅ Encontrados {len(tiff_files)} arquivos TIFF de Canelinha")
        print(f"Analisando o primeiro: {tiff_files[0].name}\n")
        diagnosticar_tiff(str(tiff_files[0]))
    else:
        print("❌ Nenhum arquivo TIFF de Canelinha encontrado")
        print("Procurando em outras cidades...")
        
        # Tentar outras cidades
        tiff_files = list(docs.glob("**/*noturna*/**/**.tif"))
        if tiff_files:
            print(f"✅ Encontrados {len(tiff_files)} arquivos TIFF em geral")
            print(f"Analisando o primeiro: {tiff_files[0].name}\n")
            diagnosticar_tiff(str(tiff_files[0]))
