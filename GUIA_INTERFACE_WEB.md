# 🌐 Interface Web - Guia Completo

## 📍 Acessar a Aplicação

```bash
python app.py
```

Abra no navegador: **http://localhost:5000**

---

## 🎯 Funcionalidades da Interface

### 1️⃣ **Análise Individual de Imagens** (Menu: Individual)

**O que faz:**
- Processa uma imagem TIFF por vez
- Mostra estatísticas detalhadas
- Valida qualidade dos dados

**Como usar:**
1. Clique em **"Individual"** (menu flutuante)
2. Selecione arquivo .tif na seção "Escolher arquivo .tif"
3. Ou faça upload de um arquivo do seu PC
4. Veja os resultados em tempo real

**Métricas exibidas:**
- ✅ Pixels válidos e percentual
- ❌ Pixels nulos (erros)
- 📭 Pixels NoData (sem cobertura)
- ⚠️ Pixels Outliers (anomalias)
- 📊 Intensidade média, mediana, min/max
- 🎯 Threshold de outliers
- 📈 **Threshold de Crescimento de Luz** (para comparações)

---

### 2️⃣ **Comparação de Crescimento de Luz** (Painel: Comparar Crescimento de Luz)

**O que faz:**
- Compara duas imagens em períodos diferentes
- Detecta mudanças de iluminação
- Classifica crescimento (Alto/Moderado/Estável/Redução)

**Como usar:**
1. Selecione **arquivo anterior** (baseline)
2. Selecione **arquivo atual** (comparação)
3. Clique em "Comparar"
4. Veja resultado com interpretação

**Interpretação:**
- 🔴 **ALTO** - Crescimento > 5%
- 🟡 **MODERADO** - Crescimento 1-5%
- 🟢 **ESTÁVEL** - Mudança < 1%
- 🔵 **REDUÇÃO** - Redução de iluminação

---

### 3️⃣ **Processamento em Lote (Paralelo)** (Menu: Lote)

**O que faz:**
- 🚀 Processa **todas as 120+ imagens em paralelo**
- ⚡ 8-10x mais rápido que sequencial (5-10 min vs 1-2 horas)
- 📊 Gera tabela com todos os resultados
- 📈 Calcula tendências de 10 anos
- 💾 Salva em CSV (sem banco de dados)

**Como usar:**
1. Clique em **"Lote"** (menu flutuante)
2. Clique em **"Iniciar Processamento Paralelo"**
3. Aguarde notificação de conclusão
4. Veja resultados em 3 abas:
   - 📋 **Tabela de Resultados** - Todos os 100+ registros
   - 📊 **Tendências por Ano** - Análise de 10 anos
   - 🧮 **Resumo Estatístico** - Média, min, max, total

**Resultados exibidos:**

#### Tabela de Resultados:
| Arquivo | Ano | Mês | Média | Threshold | Válido % |
|---------|-----|-----|-------|-----------|----------|
| bombinhas_2015_01.tif | 2015 | 1 | 82.45 | 90.12 | 97.3% |
| bombinhas_2024_12.tif | 2024 | 12 | 98.70 | 105.20 | 96.8% |

#### Tendências:
| Ano | Média | Mín | Máx | Desvio | Registros |
|-----|-------|-----|-----|--------|-----------|
| 2015 | 82.45 | 75.20 | 89.10 | 8.50 | 12 |
| 2024 | 98.70 | 92.30 | 105.20 | 9.30 | 12 |

#### Resumo Estatístico:
- **Total de Registros:** 120
- **Média Geral:** 90.58
- **Mínimo:** 75.20
- **Máximo:** 105.20

---

## 🎮 Menu Flutuante

Localizado no **canto inferior direito** da tela:

- **🖼️ Individual** - Análise de uma imagem por vez
- **⚡ Lote** - Processamento de todas as imagens

---

## 📱 Interface Responsiva

- ✅ Funciona em Desktop, Tablet e Mobile
- ✅ Menu flutuante adapta-se ao tamanho da tela
- ✅ Tabelas com scroll horizontal em telas pequenas

---

## 💾 Dados Gerados

### No Servidor (Backend):
```
resultados.csv          ← Todos os resultados (CSV)
processados.json        ← Cache (lista de processados)
tendencia_10anos.png    ← Gráfico (opcional)
comparacao_primeiro_ultimo.png  ← Gráfico (opcional)
```

### Na Interface (Frontend):
- ✅ Tabelas interativas
- ✅ Estatísticas em tempo real
- ✅ Atualização automática

---

## 🔄 Fluxo de Uso Recomendado

```
1. Abrir: http://localhost:5000
2. Menu "Individual" → Analisar 1-2 imagens
3. Menu "Lote" → Iniciar processamento
4. Esperar 5-10 minutos
5. Ver resultados em tabela
6. Comparar crescimento entre períodos
7. Exportar CSV para Excel (se necessário)
```

---

## 🎨 Cores e Status

### Status de Qualidade (Individual):
- 🟢 **✓ ACEITA** - Qualidade > 90%
- 🟡 **⚠ VERIFICAR** - Qualidade 70-90%
- 🔴 **✗ REJEITADA** - Qualidade < 70%

### Status de Crescimento (Comparação):
- 🔴 **CRESCIMENTO ALTO** - Expansão urbana significativa
- 🟡 **CRESCIMENTO MODERADO** - Desenvolvimento gradual
- 🟢 **ESTÁVEL** - Sem mudanças significativas
- 🔵 **REDUÇÃO** - Queda na iluminação

---

## ⚙️ Configurações Avançadas

### Mudar pasta monitorada:
Edite `app.py`:
```python
CAMINHO_DADOS = Path(r"seu_novo_caminho_aqui")
```

### Mudar porta:
No final do `app.py`:
```python
app.run(debug=True, port=8000)  # Mude 5000 para 8000
```

### Ativar/desativar debug:
```python
app.run(debug=False, port=5000)  # False para produção
```

---

## 🐛 Troubleshooting

### "Erro ao conectar"
```bash
# Verifique se Flask está rodando
python app.py

# Verifique a porta
http://localhost:5000
```

### "Tabela vazia"
1. Execute processamento em lote primeiro
2. Aguarde 5-10 minutos
3. Clique "Atualizar Resultados"

### "Processamento lento"
- Normal: 5-10 min para 120 imagens
- Verifique CPU: Ctrl+Shift+Esc
- Verifique espaço em disco

### "CSV não encontrado"
- Está em: `resultados.csv` (mesma pasta)
- Crie manualmente: `python processador_paralelo.py`

---

## 📊 Exemplos de Uso

### Caso 1: Verificar qualidade de uma imagem
```
1. Menu: Individual
2. Selecionar: bombinhas_2024_01.tif
3. Ler: Percentual válido, status
4. Resultado: ✓ ACEITA se > 90%
```

### Caso 2: Comparar crescimento 2015 vs 2024
```
1. Menu: Individual
2. Arquivo anterior: bombinhas_2015_01.tif
3. Arquivo atual: bombinhas_2024_01.tif
4. Comparar
5. Resultado: +16.25 (19.7% crescimento)
```

### Caso 3: Ver tendências de 10 anos
```
1. Menu: Lote
2. Iniciar processamento
3. Esperar
4. Ver tabela "Tendências por Ano"
5. Identificar anos com maior crescimento
```

---

## 💡 Dicas Úteis

1. **Primeira vez:** Comece com "Individual" para entender os dados
2. **Depois:** Use "Lote" para gerar relatório completo
3. **Análise:** Compare imagens de mesmo mês em anos diferentes
4. **Exportar:** Abra `resultados.csv` no Excel para gráficos
5. **Agendamento:** Use `automacao.py` para processar novos dados automaticamente

---

## 🎯 Resumo das Capacidades

✅ Análise individual de imagens TIFF
✅ Processamento paralelo de 100+ imagens (8-10x mais rápido)
✅ Comparação de crescimento de luz entre períodos
✅ Tendências de 10 anos
✅ Interface web responsiva
✅ Dados sem banco de dados (CSV apenas)
✅ Menu flutuante para fácil acesso
✅ Tabelas interativas e atualizáveis

---

## 🚀 Próximas Etapas

1. ✅ Explorar interface individual
2. ✅ Rodar processamento em lote
3. ✅ Analisar tendências
4. ✅ Configurar automação com `automacao.py`
5. ✅ Exportar dados para relatórios
