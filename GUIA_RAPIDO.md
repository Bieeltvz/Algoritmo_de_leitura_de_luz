# 🚀 GUIA RÁPIDO - Algoritmo de Leitura de Imagens de Satélite

## ⚡ Comece Agora (2 minutos)

### 1. Instalar dependência
```bash
pip install numpy
```

### 2. Usar no seu código
```python
from leitura_de_luz import AnalisadorLuzSatelite
import numpy as np

# Criar analisador
analisador = AnalisadorLuzSatelite()

# Sua imagem de satélite 500x500
imagem = np.load('sua_imagem.npy')  # ou imread()

# Processar
stats = analisador.processar_imagem(imagem)

# Ver resultado
print(analisador.gerar_relatorio(stats))
```

---

## 📂 Arquivos Disponíveis

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| `leitura_de_luz.py` | 🎯 Algoritmo principal | `from leitura_de_luz import AnalisadorLuzSatelite` |
| `exemplos.py` | 📚 5 exemplos práticos | `python exemplos.py` |
| `testes.py` | ✅ 25 testes unitários | `python testes.py` |
| `README.md` | 📖 Documentação detalhada | Ver configurações avançadas |
| `SUMARIO.md` | 📋 Resumo executivo | Visão geral completa |

---

## 🎯 Principais Métodos

### Processar uma imagem
```python
stats = analisador.processar_imagem(imagem_500x500)
```

### Processar múltiplas imagens
```python
resultados = analisador.processar_sequencia([img1, img2, img3])
```

### Acessar estatísticas
```python
print(f"Qualidade: {stats.percentual_valido:.2f}%")
print(f"Pixels válidos: {stats.pixels_validos}")
print(f"Pixels nulos (erros): {stats.pixels_nulos}")
print(f"Outliers detectados: {stats.pixels_outliers}")
print(f"Intensidade média: {stats.intensidade_media:.2f}")
```

### Gerar relatório
```python
print(analisador.gerar_relatorio(stats))
```

---

## 🔧 Configurações

### Padrão (recomendado)
```python
analisador = AnalisadorLuzSatelite(
    metodo_outlier='iqr',  # Intervalo Interquartil
    limiar_iqr=3.0         # Sensibilidade
)
```

### Alternativa: Z-Score
```python
analisador = AnalisadorLuzSatelite(
    metodo_outlier='zscore',
    limiar_zscore=3.0
)
```

### Mais/Menos Sensível
```python
# Detectar MAIS outliers
analisador = AnalisadorLuzSatelite(limiar_iqr=1.5)

# Detectar MENOS outliers
analisador = AnalisadorLuzSatelite(limiar_iqr=5.0)
```

---

## 📊 Verificar Qualidade

```
Qualidade da imagem:
  ✓ ACEITA       (≥ 90% pixels válidos)
  ⚠ VERIFICAR    (70-90% pixels válidos)
  ✗ REJEITADA    (< 70% pixels válidos)
```

---

## 🧪 Validar Instalação

Executar teste rápido:
```bash
python leitura_de_luz.py
```

Esperado: 3 relatórios com informações de imagens de teste

---

## 💻 Exemplos de Uso Real

### Carregar imagem TIFF/PNG
```python
from PIL import Image
imagem_pil = Image.open('satelite.png')
imagem = np.array(imagem_pil, dtype=float)
stats = analisador.processar_imagem(imagem)
```

### Processar pasta com imagens
```python
from pathlib import Path

pasta = Path('imagens_satelite')
resultados = []

for arquivo in pasta.glob('*.png'):
    img = np.array(Image.open(arquivo), dtype=float)
    stats = analisador.processar_imagem(img)
    resultados.append(stats)
    print(f"{arquivo.name}: {stats.percentual_valido:.1f}% válidos")
```

### Salvar resultados em CSV
```python
import csv

with open('analise.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Imagem', 'Válidos%', 'Nulos', 'Outliers', 'Média'])
    
    for idx, stats in enumerate(resultados, 1):
        writer.writerow([
            f'img_{idx}',
            f"{stats.percentual_valido:.2f}",
            stats.pixels_nulos,
            stats.pixels_outliers,
            f"{stats.intensidade_media:.2f}"
        ])
```

---

## ❓ FAQ

**P: A imagem precisa ser exatamente 500x500?**
R: Sim, o algoritmo foi desenvolvido para essa dimensão específica.

**P: Qual método usar, IQR ou Z-Score?**
R: IQR é mais robusto (recomendado). Use Z-Score se seus dados são normalmente distribuídos.

**P: Como aumentar/diminuir sensibilidade?**
R: Use `limiar_iqr` menor (mais sensível) ou maior (menos sensível).

**P: Pode processar 1000 imagens?**
R: Sim! O método `processar_sequencia()` processa quantas forem necessárias.

**P: Como integrar com banco de dados?**
R: Consulte exemplos no arquivo `README.md` para ver como exportar em CSV e JSON.

---

## 🎓 Entender os Resultados

### Exemplo de saída
```
📊 RESUMO DE VALIDAÇÃO:
  • Total de pixels:           250,000
  • Pixels válidos:            242,564 ( 97.03%) ← Qualidade
  • Pixels nulos (erro):         4,973 (  1.99%) ← Erros satélite
  • Pixels outliers:             2,463 (  0.99%) ← Valores muito altos

💡 ESTATÍSTICAS DE INTENSIDADE:
  • Média:                       99.48  ← Intensidade média
  • Mediana:                     99.00
  • Desvio padrão:               19.97

🚨 THRESHOLDS:
  • Limite de outlier:          194.00 ← Acima disso é outlier

📈 QUALIDADE DA IMAGEM:
  • Status geral: ✓ ACEITA ← Imagem aprovada!
```

---

## 📞 Próximos Passos

1. ✅ Verificou que está funcionando? → Use em produção
2. ❓ Precisa de customização? → Consulte `README.md`
3. 🧪 Quer testar mais? → Execute `python exemplos.py`
4. 🔍 Quer entender internamente? → Leia `testes.py`

---

**Desenvolvido em:** 17/04/2026
**Status:** ✅ Pronto para produção
**Suporte:** Todos os 25 testes passando ✅
