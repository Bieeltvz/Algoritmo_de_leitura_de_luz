# 📊 Threshold de Crescimento de Luz - Documentação

## 🎯 O que foi adicionado?

Um novo **threshold de crescimento de luz** (`threshold_crescimento_luz`) foi adicionado às estatísticas de intensidade da imagem. Este valor serve como uma **métrica de referência para comparar mudanças de iluminação entre imagens ao longo do tempo**.

### 📐 Fórmula

```
threshold_crescimento_luz = média_intensidade + (0.5 × desvio_padrão)
```

Este valor representa um "piso" de intensidade esperada que incorpora tanto a média quanto a variabilidade dos dados.

---

## 🔍 Para quê serve?

### 1. **Comparação Temporal**
Compara imagens do mesmo local em diferentes períodos:
- Detecta se houve crescimento de iluminação urbana
- Identifica padrões de expansão urbana
- Monitora mudanças em infraestrutura de iluminação

### 2. **Análise de Mudanças**
- **Crescimento significativo**: Mudanças > 5% (🔴 ALTO)
- **Crescimento moderado**: Mudanças entre 1-5% (🟡 MODERADO)  
- **Estável**: Mudanças entre -1% e 1% (🟢 ESTÁVEL)
- **Redução**: Mudanças < -1% (🔵 REDUÇÃO)

### 3. **Detecção de Anomalias**
Identifica eventos anormais como:
- Apagões ou falhas de energia
- Mudanças na infraestrutura urbana
- Problemas nos sensores de satélite

---

## 📋 Como usar?

### Passo 1: Processar Imagens
```python
from leitura_de_luz import AnalisadorLuzSatelite

analisador = AnalisadorLuzSatelite()

# Imagens de períodos diferentes
stats_periodo_1 = analisador.processar_imagem(imagem_ano_1)
stats_periodo_2 = analisador.processar_imagem(imagem_ano_2)
```

### Passo 2: Comparar Crescimento
```python
analise = analisador.comparar_crescimento_luz(stats_periodo_1, stats_periodo_2)

print(f"Status: {analise['status_crescimento']}")
print(f"Crescimento: {analise['percentual_crescimento']:.2f}%")
print(f"Threshold referência: {analise['threshold_referencia']:.2f}")
```

### Passo 3: Interpretar Resultados
O método retorna um dicionário com:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `crescimento_media` | float | Diferença absoluta na intensidade média |
| `percentual_crescimento` | float | Percentual de mudança |
| `threshold_referencia` | float | Threshold do período anterior |
| `crescimento_significativo` | bool | Se mudança é significativa (> 0.3×desvio) |
| `status_crescimento` | str | Status visual (🔴🟡🟢🔵) |
| `diferenca_thresholds` | float | Mudança no threshold entre períodos |

---

## 📊 Exemplo Prático

```python
# Dados simulados
stats_p1 = {
    'intensidade_media': 85.0,
    'threshold_crescimento_luz': 92.5,
    'desvio_padrao': 15.0
}

stats_p2 = {
    'intensidade_media': 92.0,
    'threshold_crescimento_luz': 99.5,
    'desvio_padrao': 15.0
}

# Comparação
resultado = analisador.comparar_crescimento_luz(stats_p1, stats_p2)

# Resultado:
# crescimento_media: +7.0
# percentual_crescimento: +8.24%
# status_crescimento: '🔴 CRESCIMENTO ALTO'
# threshold_referencia: 92.5
# diferenca_thresholds: +7.0
```

### Interpretação:
- ✅ Crescimento de **8.24%** em um período
- ⚠️ Status de **CRESCIMENTO ALTO** (> 5%)
- 📈 Threshold também aumentou de 92.5 para 99.5
- 💡 Indica expansão urbana significativa

---

## 🎨 Visualização no Relatório

O novo threshold aparece na seção de **THRESHOLDS**:

```
🚨 THRESHOLDS:
  • Limite de outlier:      250.00
  • Crescimento de luz:      97.50 (referência p/ comparação)
```

---

## 🧪 Executar Exemplo Completo

Um arquivo de demonstração foi criado: `exemplo_crescimento_luz.py`

```bash
python exemplo_crescimento_luz.py
```

Mostra:
1. ✅ Série temporal com 3 períodos
2. ✅ Comparações entre períodos
3. ✅ Detecção de anomalias (queda de luz)
4. ✅ Interpretação de resultados

---

## 🔧 Parâmetros Ajustáveis

Se precisar ajustar a sensibilidade, edite:

```python
# No método calcular_threshold_crescimento_luz()
# Mude de 0.5 para outro valor (quanto menor, mais sensível):
threshold_crescimento = media + (0.5 * desvio)  # ← mude 0.5 conforme necessário
```

**Exemplos:**
- `0.3`: Mais sensível (detecta mudanças pequenas)
- `0.5`: Padrão (recomendado)
- `1.0`: Menos sensível (só detecta mudanças grandes)

---

## 📚 Integração com App.py

Para integrar no aplicativo web, use:

```python
# Dentro da função que processa imagens
stats = analisador.processar_imagem(imagem)

# Acessar o novo valor
crescimento_luz = stats.threshold_crescimento_luz

# Guardar em banco de dados para comparações futuras
salvar_no_bd({
    'timestamp': datetime.now(),
    'intensidade_media': stats.intensidade_media,
    'threshold_crescimento_luz': stats.threshold_crescimento_luz,
    'percentual_valido': stats.percentual_valido
})
```

---

## ✨ Casos de Uso

1. **Monitoramento Urbano**: Acompanhar expansão de cidades
2. **Planejamento Energético**: Prever demanda por eletricidade
3. **Análise Ambiental**: Estudar impacto da poluição luminosa
4. **Infraestrutura**: Detectar falhas em sistemas de iluminação
5. **Pesquisa Geoespacial**: Correlacionar com desenvolvimento econômico

---

## 🐛 Troubleshooting

**P: Por que o threshold de crescimento é sempre maior que a média?**
R: Porque a fórmula adiciona 0.5 × desvio_padrão. Isso cria um "piso" acima da média.

**P: Qual é o significado de um crescimento negativo?**
R: Indica redução de iluminação. Pode significar economia de energia, desligamento de luzes, ou problemas técnicos.

**P: Como faço para detectar anomalias?**
R: Use `crescimento_significativo` e verifique se a mudança é maior que o esperado usando o desvio padrão como referência.

---

## 📖 Referências

- [leitura_de_luz.py](leitura_de_luz.py) - Classe principal
- [exemplo_crescimento_luz.py](exemplo_crescimento_luz.py) - Exemplos práticos
- [README.md](README.md) - Documentação geral
