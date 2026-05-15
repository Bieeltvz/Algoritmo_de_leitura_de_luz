"""
EXEMPLOS PRÁTICOS DE USO DO ALGORITMO
"""

import numpy as np
from leitura_de_luz import AnalisadorLuzSatelite
import logging

logging.basicConfig(level=logging.WARNING)  # Reduzir verbosidade


# ============================================================================
# EXEMPLO 1: Usar com imagens TIFF/PNG
# ============================================================================

def exemplo_com_arquivo_real():
    """Processar imagem de satélite real de arquivo"""
    from PIL import Image
    
    # Ler imagem
    imagem_pil = Image.open('satelite.png')
    imagem = np.array(imagem_pil, dtype=float)
    
    # Garantir que é 500x500
    if imagem.shape != (500, 500):
        imagem = np.resize(imagem, (500, 500))
    
    # Processar
    analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0)
    stats = analisador.processar_imagem(imagem)
    
    print(analisador.gerar_relatorio(stats))


# ============================================================================
# EXEMPLO 2: Simular Diferentes Cenários
# ============================================================================

def gerar_imagem_limpa():
    """Imagem com boa qualidade - poucos erros"""
    imagem = np.random.normal(loc=100, scale=10, size=(500, 500))
    imagem = np.clip(imagem, 0, 255)
    
    # Apenas 0.5% de pixels nulos
    mascara = np.random.random((500, 500)) < 0.005
    imagem[mascara] = 0
    
    return imagem.astype(float)


def gerar_imagem_com_ruido():
    """Imagem com muitos erros - qualidade ruim"""
    imagem = np.random.normal(loc=100, scale=30, size=(500, 500))
    imagem = np.clip(imagem, 0, 255)
    
    # 5% de pixels nulos
    mascara_nula = np.random.random((500, 500)) < 0.05
    imagem[mascara_nula] = 0
    
    # 3% de outliers
    mascara_outlier = np.random.random((500, 500)) < 0.03
    imagem[mascara_outlier] = np.random.uniform(240, 255, np.sum(mascara_outlier))
    
    return imagem.astype(float)


def gerar_imagem_defeituosa():
    """Imagem com muitos defeitos - deve ser rejeitada"""
    imagem = np.random.uniform(50, 200, size=(500, 500))
    
    # 15% de pixels nulos
    mascara_nula = np.random.random((500, 500)) < 0.15
    imagem[mascara_nula] = 0
    
    # 8% de outliers
    mascara_outlier = np.random.random((500, 500)) < 0.08
    imagem[mascara_outlier] = 255
    
    return imagem.astype(float)


def comparar_cenarios():
    """Compara 3 cenários diferentes"""
    print("\n" + "="*70)
    print("COMPARAÇÃO DE 3 CENÁRIOS DE QUALIDADE")
    print("="*70)
    
    analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0)
    
    cenarios = [
        ("IMAGEM LIMPA", gerar_imagem_limpa()),
        ("IMAGEM COM RUÍDO", gerar_imagem_com_ruido()),
        ("IMAGEM DEFEITUOSA", gerar_imagem_defeituosa()),
    ]
    
    for nome, imagem in cenarios:
        print(f"\n{'─'*70}")
        print(f"Cenário: {nome}")
        print(f"{'─'*70}")
        stats = analisador.processar_imagem(imagem)
        print(analisador.gerar_relatorio(stats))


# ============================================================================
# EXEMPLO 3: Análise de Sequência Temporal
# ============================================================================

def analisar_serie_temporal():
    """Simula observação de uma região ao longo do tempo"""
    print("\n" + "="*70)
    print("ANÁLISE DE SÉRIE TEMPORAL (12 imagens)")
    print("="*70)
    
    analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0)
    
    # Gerar 12 imagens simulando mudanças ao longo do tempo
    imagens = []
    for mes in range(12):
        # Intensidade varia ao longo do ano
        intensidade_media = 100 + 20 * np.sin(2 * np.pi * mes / 12)
        imagem = np.random.normal(loc=intensidade_media, scale=15, size=(500, 500))
        imagem = np.clip(imagem, 0, 255)
        
        # Adicionar ruído variável
        pct_erro = 0.02 + 0.01 * np.sin(2 * np.pi * mes / 12)
        mascara_erro = np.random.random((500, 500)) < pct_erro
        imagem[mascara_erro] = 0
        
        imagens.append(imagem.astype(float))
    
    # Processar
    resultados = analisador.processar_sequencia(imagens)
    
    # Resumo
    print("\n" + "─"*70)
    print("RESUMO DA SÉRIE TEMPORAL")
    print("─"*70)
    print(f"{'Mês':<6} {'Válidos':<12} {'Média':<12} {'Desvio':<12} {'Status':<15}")
    print("-" * 70)
    
    for mes, stats in enumerate(resultados, 1):
        status = "✓ ACEITA" if stats.percentual_valido >= 90 else "⚠ VERIFICAR" if stats.percentual_valido >= 70 else "✗ REJEITADA"
        print(f"{mes:<6} {stats.percentual_valido:>10.2f}% {stats.intensidade_media:>11.2f} {stats.desvio_padrao:>11.2f} {status:<15}")


# ============================================================================
# EXEMPLO 4: Métodos Comparativos
# ============================================================================

def comparar_metodos_outlier():
    """Compara IQR vs Z-Score para detecção de outliers"""
    print("\n" + "="*70)
    print("COMPARAÇÃO: IQR vs Z-Score")
    print("="*70)
    
    imagem = np.random.normal(loc=100, scale=20, size=(500, 500))
    imagem = np.clip(imagem, 0, 255)
    
    # Adicionar alguns valores extremos
    mascara = np.random.random((500, 500)) < 0.02
    imagem[mascara] = np.random.uniform(200, 255, np.sum(mascara))
    
    # Método IQR
    analisador_iqr = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0)
    stats_iqr = analisador_iqr.processar_imagem(imagem)
    
    # Método Z-Score
    analisador_zscore = AnalisadorLuzSatelite(metodo_outlier='zscore', limiar_zscore=3.0)
    stats_zscore = analisador_zscore.processar_imagem(imagem)
    
    # Comparação
    print(f"\n{'Métrica':<25} {'IQR':<20} {'Z-Score':<20}")
    print("-" * 65)
    print(f"{'Threshold':<25} {stats_iqr.threshold_outlier:>18.2f} {stats_zscore.threshold_outlier:>18.2f}")
    print(f"{'Pixels Outliers':<25} {stats_iqr.pixels_outliers:>18,} {stats_zscore.pixels_outliers:>18,}")
    print(f"{'Pixels Válidos':<25} {stats_iqr.pixels_validos:>18,} {stats_zscore.pixels_validos:>18,}")
    print(f"{'Intensidade Média':<25} {stats_iqr.intensidade_media:>18.2f} {stats_zscore.intensidade_media:>18.2f}")
    print(f"{'Percentual Válido':<25} {stats_iqr.percentual_valido:>17.2f}% {stats_zscore.percentual_valido:>17.2f}%")
    print(f"{'Status':<25} {'ACEITA' if stats_iqr.percentual_valido >= 90 else 'VERIFICAR':>18} {'ACEITA' if stats_zscore.percentual_valido >= 90 else 'VERIFICAR':>18}")


# ============================================================================
# EXEMPLO 5: Processamento em Lote
# ============================================================================

def processar_lote_com_filtro():
    """Processa múltiplas imagens e filtra as boas"""
    print("\n" + "="*70)
    print("PROCESSAMENTO EM LOTE COM FILTRO DE QUALIDADE")
    print("="*70)
    
    analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0)
    
    # Gerar 10 imagens com qualidades variadas
    imagens = []
    for i in range(10):
        if i < 3:  # Primeiras 3: qualidade boa
            imagem = gerar_imagem_limpa()
        elif i < 6:  # Próximas 3: qualidade média
            imagem = gerar_imagem_com_ruido()
        else:  # Últimas 4: qualidade ruim
            imagem = gerar_imagem_defeituosa()
        imagens.append(imagem)
    
    resultados = analisador.processar_sequencia(imagens)
    
    # Separar por qualidade
    boas = []
    intermedias = []
    ruins = []
    
    for idx, stats in enumerate(resultados):
        if stats.percentual_valido >= 90:
            boas.append(idx + 1)
        elif stats.percentual_valido >= 70:
            intermedias.append(idx + 1)
        else:
            ruins.append(idx + 1)
    
    print(f"\n✓ Imagens BOM: {boas} ({len(boas)} no total)")
    print(f"⚠ Imagens INTERMEDIÁRIAS: {intermedias} ({len(intermedias)} no total)")
    print(f"✗ Imagens RUINS: {ruins} ({len(ruins)} no total)")
    print(f"\nAproveitamento: {len(boas)}/{len(imagens)} imagens ({100*len(boas)/len(imagens):.1f}%)")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "EXEMPLOS DE USO DO ALGORITMO" + " "*25 + "║")
    print("╚" + "═"*68 + "╝")
    
    # Executar exemplos
    comparar_cenarios()
    comparar_metodos_outlier()
    analisar_serie_temporal()
    processar_lote_com_filtro()
    
    print("\n" + "="*70)
    print("✓ Todos os exemplos foram executados com sucesso!")
    print("="*70 + "\n")
