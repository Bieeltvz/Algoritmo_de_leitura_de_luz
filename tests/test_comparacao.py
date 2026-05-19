"""
Script de teste para o método comparar_crescimento_luz
"""

import numpy as np
from leitura_de_luz import AnalisadorLuzSatelite, EstatisticasImagem

# Criar analisador
analisador = AnalisadorLuzSatelite()

# Simular estatísticas de duas imagens
stats_anterior = EstatisticasImagem(
    total_pixels=250000,
    pixels_validos=240000,
    pixels_nulos=5000,
    pixels_outliers=5000,
    pixels_nodata=0,
    percentual_valido=96.0,
    intensidade_media=75.5,
    intensidade_mediana=74.2,
    intensidade_minima=10.0,
    intensidade_maxima=240.0,
    desvio_padrao=18.5,
    threshold_outlier=250.0,
    threshold_crescimento_luz=84.75  # 75.5 + 0.5*18.5
)

stats_atual = EstatisticasImagem(
    total_pixels=250000,
    pixels_validos=245000,
    pixels_nulos=3000,
    pixels_outliers=2000,
    pixels_nodata=0,
    percentual_valido=98.0,
    intensidade_media=82.3,
    intensidade_mediana=81.5,
    intensidade_minima=12.0,
    intensidade_maxima=245.0,
    desvio_padrao=16.8,
    threshold_outlier=250.0,
    threshold_crescimento_luz=90.7  # 82.3 + 0.5*16.8
)

# Comparar crescimento
resultado = analisador.comparar_crescimento_luz(stats_anterior, stats_atual)

print("=" * 70)
print("RESULTADO DA COMPARAÇÃO DE CRESCIMENTO DE LUZ")
print("=" * 70)
print(f"\n📊 Crescimento de Intensidade:")
print(f"   Absoluto: {resultado['crescimento_media']:+.2f}")
print(f"   Percentual: {resultado['percentual_crescimento']:+.2f}%")
print(f"\n🎯 Status: {resultado['status_crescimento']}")
print(f"✓ Significativo: {resultado['crescimento_significativo']}")
print(f"\n📈 Diferença de Thresholds: {resultado['diferenca_thresholds']:+.2f}")
print(f"\n📝 Qualidade da Análise: {resultado['detalhes']['qualidade_analise']}")

print("\n" + "=" * 70)
print("DETALHES COMPLETOS")
print("=" * 70)
for chave, valor in resultado['detalhes'].items():
    if isinstance(valor, float):
        print(f"  {chave:.<40} {valor:>10.2f}")
    else:
        print(f"  {chave:.<40} {valor:>10}")

print(f"\n✅ Teste concluído com sucesso!")
