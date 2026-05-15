"""
Exemplo de uso do threshold de crescimento de luz para análise de mudanças urbanas
Demonstra como comparar intensidades de luz entre duas imagens de satélite
"""

import numpy as np
from leitura_de_luz import AnalisadorLuzSatelite

def gerar_imagem_com_intensidade(intensidade_base: float, variacao: float = 20, 
                                 percentual_nulos: float = 0.02) -> np.ndarray:
    """
    Gera uma imagem simulada com intensidade específica
    
    Args:
        intensidade_base: Valor médio de intensidade
        variacao: Desvio padrão da distribuição
        percentual_nulos: Percentual de pixels nulos (erro do satélite)
    """
    imagem = np.random.normal(loc=intensidade_base, scale=variacao, size=(500, 500))
    imagem = np.clip(imagem, 0, 255).astype(np.float32)
    
    # Adicionar pixels nulos (erros do satélite)
    mascara_nula = np.random.random((500, 500)) < percentual_nulos
    imagem[mascara_nula] = 0
    
    # Adicionar alguns outliers (1%)
    mascara_outlier = np.random.random((500, 500)) < 0.01
    imagem[mascara_outlier] = np.random.randint(230, 256, np.sum(mascara_outlier))
    
    return imagem


def exemplo_comparacao_temporal():
    """
    Exemplo: Análise de crescimento de luz em uma cidade ao longo de 3 períodos
    """
    print("\n" + "="*70)
    print("ANÁLISE DE CRESCIMENTO DE LUZ - SÉRIE TEMPORAL")
    print("="*70)
    
    analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0)
    
    # Simular 3 imagens em sequência temporal (crescimento gradual de luz)
    # Período 1: Baseline (cidade com iluminação padrão)
    # Período 2: Crescimento moderado
    # Período 3: Crescimento acentuado
    
    print("\n📡 Gerando imagens simuladas com crescimento de luz...")
    
    imagem_periodo_1 = gerar_imagem_com_intensidade(intensidade_base=85, variacao=18)
    imagem_periodo_2 = gerar_imagem_com_intensidade(intensidade_base=92, variacao=18)
    imagem_periodo_3 = gerar_imagem_com_intensidade(intensidade_base=105, variacao=18)
    
    # Processar cada período
    print("\n📊 Processando imagens...")
    stats_p1 = analisador.processar_imagem(imagem_periodo_1)
    stats_p2 = analisador.processar_imagem(imagem_periodo_2)
    stats_p3 = analisador.processar_imagem(imagem_periodo_3)
    
    # Exibir relatórios individuais
    print("\n" + "-"*70)
    print("PERÍODO 1 (BASELINE - Ano 1)")
    print("-"*70)
    print(analisador.gerar_relatorio(stats_p1))
    
    print("\n" + "-"*70)
    print("PERÍODO 2 (Ano 2)")
    print("-"*70)
    print(analisador.gerar_relatorio(stats_p2))
    
    print("\n" + "-"*70)
    print("PERÍODO 3 (Ano 3)")
    print("-"*70)
    print(analisador.gerar_relatorio(stats_p3))
    
    # Comparar crescimento entre períodos
    print("\n" + "="*70)
    print("📈 ANÁLISE DE CRESCIMENTO DE LUZ")
    print("="*70)
    
    comparacao_p1_p2 = analisador.comparar_crescimento_luz(stats_p1, stats_p2)
    comparacao_p2_p3 = analisador.comparar_crescimento_luz(stats_p2, stats_p3)
    
    print("\n🔄 PERÍODO 1 → PERÍODO 2:")
    print(f"  Status:                {comparacao_p1_p2['status_crescimento']}")
    print(f"  Crescimento média:     {comparacao_p1_p2['crescimento_media']:>+8.2f} unidades")
    print(f"  Crescimento %:         {comparacao_p1_p2['percentual_crescimento']:>+8.2f}%")
    print(f"  Threshold ref (P1):    {comparacao_p1_p2['threshold_referencia']:>8.2f}")
    print(f"  Threshold novo (P2):   {stats_p2.threshold_crescimento_luz:>8.2f}")
    print(f"  Significativo:         {'Sim ✓' if comparacao_p1_p2['crescimento_significativo'] else 'Não'}")
    
    print("\n🔄 PERÍODO 2 → PERÍODO 3:")
    print(f"  Status:                {comparacao_p2_p3['status_crescimento']}")
    print(f"  Crescimento média:     {comparacao_p2_p3['crescimento_media']:>+8.2f} unidades")
    print(f"  Crescimento %:         {comparacao_p2_p3['percentual_crescimento']:>+8.2f}%")
    print(f"  Threshold ref (P2):    {comparacao_p2_p3['threshold_referencia']:>8.2f}")
    print(f"  Threshold novo (P3):   {stats_p3.threshold_crescimento_luz:>8.2f}")
    print(f"  Significativo:         {'Sim ✓' if comparacao_p2_p3['crescimento_significativo'] else 'Não'}")
    
    # Resumo geral
    print("\n" + "="*70)
    print("📊 RESUMO GERAL")
    print("="*70)
    crescimento_total = stats_p3.intensidade_media - stats_p1.intensidade_media
    percentual_total = (crescimento_total / stats_p1.intensidade_media * 100)
    
    print(f"\n  Período 1 → Período 3:")
    print(f"    • Média inicial:           {stats_p1.intensidade_media:.2f}")
    print(f"    • Média final:             {stats_p3.intensidade_media:.2f}")
    print(f"    • Crescimento total:       {crescimento_total:+.2f} unidades ({percentual_total:+.2f}%)")
    print(f"    • Threshold Período 1:     {stats_p1.threshold_crescimento_luz:.2f}")
    print(f"    • Threshold Período 3:     {stats_p3.threshold_crescimento_luz:.2f}")
    print(f"    • Mudança de threshold:    {stats_p3.threshold_crescimento_luz - stats_p1.threshold_crescimento_luz:+.2f}")
    
    # Interpretação
    print("\n💡 INTERPRETAÇÃO:")
    if percentual_total > 10:
        print("   ⚠️  CRESCIMENTO ALTO DE LUZ: Indicativo de forte expansão urbana")
    elif percentual_total > 5:
        print("   🟡 CRESCIMENTO MODERADO: Desenvolvimento urbano em curso")
    elif percentual_total > 1:
        print("   🟢 CRESCIMENTO LEVE: Pequena variação na iluminação")
    else:
        print("   🔵 ESTÁVEL: Pouca ou nenhuma mudança na iluminação")


def exemplo_deteccao_anomalia():
    """
    Exemplo: Detecção de anomalia de crescimento (queda repentina)
    """
    print("\n\n" + "="*70)
    print("DETECÇÃO DE ANOMALIA - QUEDA REPENTINA DE LUZ")
    print("="*70)
    
    analisador = AnalisadorLuzSatelite(metodo_outlier='iqr')
    
    print("\n📡 Gerando cenário: Crescimento normal seguido de queda...")
    
    # Crescimento normal
    img_normal_1 = gerar_imagem_com_intensidade(80)
    img_normal_2 = gerar_imagem_com_intensidade(90)
    
    # Queda anômala (simula apagão ou mudança de infra)
    img_anomalia = gerar_imagem_com_intensidade(60)
    
    stats_1 = analisador.processar_imagem(img_normal_1)
    stats_2 = analisador.processar_imagem(img_normal_2)
    stats_3 = analisador.processar_imagem(img_anomalia)
    
    comp_normal = analisador.comparar_crescimento_luz(stats_1, stats_2)
    comp_anomalia = analisador.comparar_crescimento_luz(stats_2, stats_3)
    
    print(f"\n  Fase normal (P1→P2):      {comp_normal['status_crescimento']}")
    print(f"    Crescimento:           {comp_normal['percentual_crescimento']:+.2f}%")
    
    print(f"\n  Fase anômala (P2→P3):    {comp_anomalia['status_crescimento']}")
    print(f"    Crescimento:           {comp_anomalia['percentual_crescimento']:+.2f}%")
    print(f"    ⚠️  ALERTA: Redução inesperada de luz detectada!")


if __name__ == "__main__":
    exemplo_comparacao_temporal()
    exemplo_deteccao_anomalia()
    
    print("\n" + "="*70)
    print("✅ Exemplos concluídos!")
    print("="*70)
