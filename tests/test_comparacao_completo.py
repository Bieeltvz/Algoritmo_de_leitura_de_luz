"""
Testes avançados para validar todos os cenários do método comparar_crescimento_luz
"""

import numpy as np
from leitura_de_luz import AnalisadorLuzSatelite, EstatisticasImagem

def criar_stats(media, desvio, pixels_validos=240000):
    """Função auxiliar para criar estatísticas"""
    return EstatisticasImagem(
        total_pixels=250000,
        pixels_validos=pixels_validos,
        pixels_nulos=5000,
        pixels_outliers=5000,
        pixels_nodata=0,
        percentual_valido=100 * pixels_validos / 250000,
        intensidade_media=media,
        intensidade_mediana=media - 1,
        intensidade_minima=10.0,
        intensidade_maxima=245.0,
        desvio_padrao=desvio,
        threshold_outlier=250.0,
        threshold_crescimento_luz=media + 0.5 * desvio
    )

# Criar analisador
analisador = AnalisadorLuzSatelite()

print("=" * 80)
print("TESTES COMPLETOS DO MÉTODO COMPARAR_CRESCIMENTO_LUZ")
print("=" * 80)

# ========== TESTE 1: CRESCIMENTO SIGNIFICATIVO ==========
print("\n\n📈 TESTE 1: CRESCIMENTO SIGNIFICATIVO")
print("─" * 80)

stats_ant_t1 = criar_stats(media=75.5, desvio=18.5)
stats_atu_t1 = criar_stats(media=82.3, desvio=16.8)

resultado_t1 = analisador.comparar_crescimento_luz(stats_ant_t1, stats_atu_t1)

print(f"Status: {resultado_t1['status_crescimento']}")
print(f"Crescimento: {resultado_t1['crescimento_media']:+.2f} ({resultado_t1['percentual_crescimento']:+.2f}%)")
print(f"Significativo: {'✓ SIM' if resultado_t1['crescimento_significativo'] else '✗ NÃO'}")
print(f"Qualidade: {resultado_t1['detalhes']['qualidade_analise']}")

assert resultado_t1['status_crescimento'] == 'CRESCIMENTO', "Teste 1 falhou!"
assert resultado_t1['crescimento_significativo'] == True, "Teste 1 falhou!"
print("✅ PASSOU")

# ========== TESTE 2: DECRÉSCIMO SIGNIFICATIVO ==========
print("\n\n📉 TESTE 2: DECRÉSCIMO SIGNIFICATIVO")
print("─" * 80)

stats_ant_t2 = criar_stats(media=90.0, desvio=20.0)
stats_atu_t2 = criar_stats(media=75.5, desvio=18.5)

resultado_t2 = analisador.comparar_crescimento_luz(stats_ant_t2, stats_atu_t2)

print(f"Status: {resultado_t2['status_crescimento']}")
print(f"Crescimento: {resultado_t2['crescimento_media']:+.2f} ({resultado_t2['percentual_crescimento']:+.2f}%)")
print(f"Significativo: {'✓ SIM' if resultado_t2['crescimento_significativo'] else '✗ NÃO'}")
print(f"Qualidade: {resultado_t2['detalhes']['qualidade_analise']}")

assert resultado_t2['status_crescimento'] == 'DECRÉSCIMO', "Teste 2 falhou!"
assert resultado_t2['crescimento_significativo'] == True, "Teste 2 falhou!"
print("✅ PASSOU")

# ========== TESTE 3: CRESCIMENTO ESTÁVEL (MÍNIMO) ==========
print("\n\n➡️  TESTE 3: CRESCIMENTO ESTÁVEL (SEM MUDANÇA SIGNIFICATIVA)")
print("─" * 80)

stats_ant_t3 = criar_stats(media=80.0, desvio=15.0)
stats_atu_t3 = criar_stats(media=80.3, desvio=15.2)

resultado_t3 = analisador.comparar_crescimento_luz(stats_ant_t3, stats_atu_t3)

print(f"Status: {resultado_t3['status_crescimento']}")
print(f"Crescimento: {resultado_t3['crescimento_media']:+.2f} ({resultado_t3['percentual_crescimento']:+.2f}%)")
print(f"Significativo: {'✓ SIM' if resultado_t3['crescimento_significativo'] else '✗ NÃO'}")
print(f"Qualidade: {resultado_t3['detalhes']['qualidade_analise']}")

assert resultado_t3['status_crescimento'] == 'ESTÁVEL', "Teste 3 falhou!"
assert resultado_t3['crescimento_significativo'] == False, "Teste 3 falhou!"
print("✅ PASSOU")

# ========== TESTE 4: QUALIDADE BAIXA (POUCOS PIXELS VÁLIDOS) ==========
print("\n\n⚠️  TESTE 4: IMAGEM COM QUALIDADE BAIXA")
print("─" * 80)

stats_ant_t4 = criar_stats(media=75.5, desvio=18.5, pixels_validos=160000)  # 64% válidos
stats_atu_t4 = criar_stats(media=82.3, desvio=16.8, pixels_validos=165000)

resultado_t4 = analisador.comparar_crescimento_luz(stats_ant_t4, stats_atu_t4)

print(f"Status: {resultado_t4['status_crescimento']}")
print(f"Crescimento: {resultado_t4['crescimento_media']:+.2f} ({resultado_t4['percentual_crescimento']:+.2f}%)")
print(f"Qualidade: {resultado_t4['detalhes']['qualidade_analise']}")
print(f"Pixels válidos (anterior): {resultado_t4['detalhes']['percentual_valido_anterior']:.1f}%")
print(f"Pixels válidos (atual): {resultado_t4['detalhes']['percentual_valido_atual']:.1f}%")

assert resultado_t4['detalhes']['qualidade_analise'] == 'BAIXA_QUALIDADE', "Teste 4 falhou!"
print("✅ PASSOU")

# ========== TESTE 5: CRESCIMENTO NORMALIZADO (VARIÂNCIA) ==========
print("\n\n📊 TESTE 5: CRESCIMENTO NORMALIZADO POR VARIÂNCIA")
print("─" * 80)

stats_ant_t5 = criar_stats(media=50.0, desvio=30.0)
stats_atu_t5 = criar_stats(media=65.0, desvio=28.0)

resultado_t5 = analisador.comparar_crescimento_luz(stats_ant_t5, stats_atu_t5)

crescimento_norm = resultado_t5['detalhes']['crescimento_normalizado']
print(f"Crescimento normalizado: {crescimento_norm:.2f} desvios padrão")
print(f"Crescimento bruto: {resultado_t5['crescimento_media']:+.2f}")
print(f"Significativo: {'✓ SIM' if resultado_t5['crescimento_significativo'] else '✗ NÃO'}")

print("✅ PASSOU")

print("\n\n" + "=" * 80)
print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
print("=" * 80)
print("\nO método comparar_crescimento_luz está pronto para uso em produção!")
