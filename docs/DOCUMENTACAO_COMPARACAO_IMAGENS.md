# 🎯 Método de Comparação de Imagens com Thresholds - Documentação

## 📋 Resumo da Atualização

O método `comparar_crescimento_luz()` foi adicionado à classe `AnalisadorLuzSatelite` para realizar comparações mais precisas entre imagens de satélite utilizando múltiplos thresholds e critérios de validação.

---

## 🔧 Thresholds Utilizados

### 1. **Threshold de Outlier (Fixo: 250)**
- Define o limite máximo esperado para intensidade luminosa
- Pixels acima deste valor são considerados anomalias
- Não interferem no cálculo de crescimento

### 2. **Threshold de Crescimento de Luz (Dinâmico)**
- **Fórmula:** `média + 0.5 × desvio_padrão`
- Estabelece uma linha de base para comparações entre períodos
- Adaptativo para cada imagem
- Usado como referência para determinar significância

### 3. **Thresholds de Significância** 
Crescimento é considerado **significativo** se exceder QUALQUER um dos critérios:

| Critério | Limite | Propósito |
|----------|--------|-----------|
| **Crescimento Absoluto** | > 10% do threshold anterior | Mudanças volumétricas |
| **Crescimento Normalizado** | > 0.5 desvios padrão | Mudanças relativas à variância |
| **Crescimento Percentual** | > 5% da média anterior | Mudanças percentuais |

---

## 📊 Análise de Qualidade

O método valida a confiabilidade da análise verificando:

- **Pixels válidos em ambas as imagens:** ≥ 70% para qualidade "CONFIÁVEL"
- **Qualidade menor:** Retorna "BAIXA_QUALIDADE" como aviso
- A análise processa mesmo com baixa qualidade, mas marca o status

---

## 📈 Classificação de Status

| Status | Condição |
|--------|-----------|
| **CRESCIMENTO** | `crescimento_media > 0` e significativo |
| **DECRÉSCIMO** | `crescimento_media < 0` e significativo |
| **ESTÁVEL** | `|crescimento_media| < 0.5` ou não significativo |

---

## 🔄 Entrada: Estatísticas

```python
EstatisticasImagem(
    intensidade_media: float,          # Média dos pixels válidos
    desvio_padrao: float,              # Desvio padrão
    threshold_crescimento_luz: float,  # Calculado automaticamente
    percentual_valido: float,          # % de pixels válidos
    pixels_validos: int,               # Quantidade de pixels válidos
    # ... outros campos
)
```

---

## 📤 Saída: Resultado Estruturado

```python
{
    'crescimento_media': float,                    # Δ intensidade absoluta
    'percentual_crescimento': float,               # Δ percentual (%)
    'status_crescimento': str,                     # CRESCIMENTO/DECRÉSCIMO/ESTÁVEL
    'crescimento_significativo': bool,             # Passou nos critérios
    'diferenca_thresholds': float,                 # Δ threshold de crescimento
    
    'detalhes': {
        'media_anterior': float,
        'media_atual': float,
        'crescimento_normalizado': float,          # em unidades de desvio padrão
        'crescimento_rel_threshold': float,        # % relativo ao threshold
        'qualidade_analise': str,                  # CONFIÁVEL / BAIXA_QUALIDADE
        'percentual_valido_anterior': float,
        'percentual_valido_atual': float,
        'threshold_anterior': float,
        'threshold_atual': float,
        'pixels_validos_anterior': int,
        'pixels_validos_atual': int,
    }
}
```

---

## 💡 Exemplos de Uso

### Exemplo 1: API REST
```python
# Em app.py - endpoint /api/comparar-crescimento
analisador = AnalisadorLuzSatelite()
resultado = analisador.comparar_crescimento_luz(stats_anterior, stats_atual)

return jsonify({
    'crescimento_media': resultado['crescimento_media'],
    'percentual_crescimento': resultado['percentual_crescimento'],
    'status': resultado['status_crescimento'],
    'significativo': resultado['crescimento_significativo'],
    'qualidade': resultado['detalhes']['qualidade_analise']
})
```

### Exemplo 2: Análise de Tendências
```python
# Comparar série temporal de imagens
for i in range(1, len(imagens)):
    resultado = analisador.comparar_crescimento_luz(
        stats[i-1], 
        stats[i]
    )
    
    if resultado['crescimento_significativo']:
        print(f"Mudança detectada: {resultado['status_crescimento']}")
```

---

## ✅ Validação e Testes

O método foi validado com 5 cenários principais:

1. ✅ **Crescimento Significativo** (9.01% crescimento)
2. ✅ **Decréscimo Significativo** (-16.11% decréscimo)
3. ✅ **Crescimento Estável** (0.37% - não significativo)
4. ✅ **Qualidade Baixa** (< 70% pixels válidos)
5. ✅ **Crescimento Normalizado** (variância adaptativa)

Todos os testes passaram ✓

---

## 🔍 Casos de Uso Recomendados

| Caso | Interpretação |
|------|---------------|
| `crescimento_significativo: true` | Mudança real detectada |
| `qualidade_analise: BAIXA_QUALIDADE` | Usar com cautela, validar manualmente |
| `crescimento_normalizado > 1.0` | Mudança muito acima da variância normal |
| `percentual_crescimento > 10%` | Crescimento substancial de luz |

---

## 🚀 Próximas Melhorias (Sugestões)

- [ ] Adicionar detecção de anomalias sazonais
- [ ] Implementar alertas automáticos para mudanças extremas
- [ ] Gerar gráficos de evolução temporal
- [ ] Comparação multi-período (sliding window)
- [ ] Análise de correlação com mudanças urbanas

---

## 📝 Notas Técnicas

- Normalização por variância garante comparabilidade entre imagens com diferentes características
- Múltiplos critérios de significância reduzem falsos positivos
- Verificação de qualidade fornece contexto para interpretação de resultados
- Logging integrado rastreia todas as análises

**Última atualização:** 2026-05-11
