# 🌅 Algoritmo de Leitura de Luz de Satélite

Análise de crescimento de iluminação urbana em cidades do Vale do Itajaí usando imagens GeoTIFF de satélite.

## 📋 O Que É?

Sistema completo para:
- 📊 **Processar** imagens TIFF de satélite do Google Earth Engine
- 📈 **Detectar** crescimento de iluminação ao longo do tempo
- 🗺️ **Gerar** mapas interativos com heatmaps
- 🎬 **Criar** timelapses animados
- 📉 **Analisar** tendências de urbanização

**Cobertura:** 56+ cidades do Vale do Itajaí, SC  
**Período:** 2013-2023  
**Resolução:** 30m por pixel (Landsat 8)  

---

## 🚀 Como Começar

### 1️⃣ Instalação Rápida

```bash
# Clonar ou extrair o projeto
cd Algoritmo_de_leitura_de_luz

# Instalar dependências
pip install -r requirements.txt
```

### 2️⃣ Usar a Interface Web (Recomendado ⭐)

```bash
python app/app.py
```

Abrir: **http://localhost:5000**

**Recursos:**
- ✅ Selecionar cidade e pasta de imagens
- ✅ Gerar mapa interativo com heatmap
- ✅ Criar timelapse animado
- ✅ Visualizar crescimento percentual

### 3️⃣ Usar CLI (main.py)

```bash
python main.py

# Menu interativo:
# [1] Processar imagens
# [2] Gerar timelapse
# [3] Gerar mapa
# [4] Analisar tendências
# [5] Sair
```

---

## 📁 Estrutura do Projeto

```
projeto/
├── 🔧 src/                      # Código-fonte organizado
│   ├── processamento/           # Processamento de imagens
│   │   ├── leitura_de_luz.py   # 🔑 Algoritmo principal
│   │   └── processador_paralelo.py
│   ├── mapas/                  # Geração de mapas
│   │   ├── mapa_crescimento.py  # 🔑 Mapas e timelapses
│   │   └── heatmap_crescimento.py
│   ├── analise/                # Análises
│   │   └── tendencias.py       # 📈 Análise de tendências
│   ├── utils/                  # Utilitários
│   └── visualizacao/           # Visualização
│
├── 📊 data/                     # Dados
│   ├── entrada/                # Dados de entrada (vazio - use GEE)
│   ├── saida/                  # 60+ resultados.csv processados
│   ├── cache/                  # Cache de processamentos
│   └── coordenadas/            # 4 arquivos JSON de coordenadas
│
├── 🌐 app/                      # Interface Flask
│   ├── app.py                  # 🔑 Servidor web
│   ├── templates/              # HTML
│   └── static/                 # CSS, JS
│
├── 📚 docs/                     # Documentação (22 guias)
├── 🧪 tests/                    # Testes e debug
├── 📤 outputs/                  # Arquivos gerados (HTML, PNG)
│
├── 🔑 main.py                   # Entrada CLI
├── 🔑 app.py (na raiz)          # Link para app/app.py
├── setup_path.py               # Configuração de imports
├── GUIA_IMPORTS.md            # Como importar módulos
├── requirements.txt            # Dependências
└── README.md                   # Este arquivo
```

---

## 📖 Documentação

### Guias Essenciais
- **[GUIA_RAPIDO.md](docs/GUIA_RAPIDO.md)** - Comece aqui! (5 min)
- **[GUIA_INTERFACE_WEB.md](docs/GUIA_INTERFACE_WEB.md)** - Como usar a web
- **[GUIA_IMPORTS.md](GUIA_IMPORTS.md)** - Como importar módulos

### Guias Técnicos
- **[GUIA_PARALELO_SEM_BD.md](docs/GUIA_PARALELO_SEM_BD.md)** - Processamento paralelo
- **[GUIA_SELECAO_PASTAS.md](docs/GUIA_SELECAO_PASTAS.md)** - Estrutura de dados
- **[DESCOBERTA_AUTOMATICA_CIDADES.md](docs/DESCOBERTA_AUTOMATICA_CIDADES.md)** - Automação

### Informações Técnicas
- **[DOCUMENTACAO_COMPARACAO_IMAGENS.md](docs/DOCUMENTACAO_COMPARACAO_IMAGENS.md)** - Algoritmo
- **[README_ESTRUTURA.md](docs/README_ESTRUTURA.md)** - Estrutura nova
- **[INSTRUCOES_TESTE.md](docs/INSTRUCOES_TESTE.md)** - Testes

---

## 🔧 Módulos Principais

### 📊 `leitura_de_luz.py`
**Algoritmo principal de processamento**

```python
from leitura_de_luz import AnalisadorLuzSatelite

analisador = AnalisadorLuzSatelite()
resultado = analisador.processar_imagem(
    caminho_tiff='caminho/imagem.tif',
    salvar_csv=True
)
```

**Saída:**
- CSV com: `ano, intensidade_media`
- PNG com visualização
- Valor de crescimento percentual

### 🗺️ `mapa_crescimento.py`
**Geração de mapas e timelapses**

```python
from mapa_crescimento import MapaCrescimento

mapa = MapaCrescimento()

# Mapa interativo
mapa.gerar_relatorio_html_cidade('Brusque', 'saida.html')

# Timelapse
mapa.gerar_timelapse_cidade('Brusque', 'caminho_recortes', 'video.html')

# Análise de crescimento
resultado = mapa.calcular_crescimento_cidade_unica('Brusque')
print(f"Crescimento: {resultado['crescimento_percentual']}%")
```

### 📈 `processador_paralelo.py`
**Processamento paralelo de múltiplas cidades**

```python
from processador_paralelo import ProcessadorParalelo

processador = ProcessadorParalelo(
    pasta_raiz='C:/Users/.../Documents',
    num_workers=4
)

processador.processar_todas_cidades()
```

### 📉 `tendencias.py`
**Análise de tendências**

```python
from tendencias import AnalisadorTendencias

analisador = AnalisadorTendencias()
tendencia = analisador.analisar_cidade('Brusque')
print(tendencia)  # Taxa de crescimento, previsão, etc
```

---

## 📊 Dados Disponíveis

### Coordenadas (em `data/coordenadas/`)
- `coordenadas_cidades_completas_nominatim.json` - 56 cidades ⭐
- Backup: IBGE, Nominatim precision

### Resultados Processados (em `data/saida/`)
- `resultados_Brusque.csv` - Ano e intensidade
- 60+ arquivos similares para outras cidades
- Formato: CSV com headers `ano,intensidade_media`

### Timelapses e Mapas (em `outputs/`)
- `timelapse_Brusque.html` - 18-24 MB com video
- `mapa_Brusque.html` - ~10 KB com heatmap
- PNGs com visualizações estáticas

---

## ⚙️ Configuração

### Paths Importantes (em `app.py`)

```python
# 1. Definir local das imagens TIFF
CAMINHO_DOCUMENTOS = Path(r"C:\Users\USUARIO\Documents")

# 2. Coordenadas estão em
COORDENADAS_JSON = "data/coordenadas/coordenadas_cidades_completas_nominatim.json"

# 3. Resultados salvos em
PASTA_SAIDA = "data/saida"
```

### Limiares de Detecção (em `leitura_de_luz.py`)

```python
# Valores padrão (você pode ajustar)
LIMIAR_CRESCIMENTO_AMARELO = 0.13  # 13%
LIMIAR_CRESCIMENTO_VERMELHO = 0.15  # 15%
VALOR_MAXIMO_PIXEL = 3000  # Para normalização
```

---

## 🧪 Testes

```bash
# Ver arquivos de teste
ls tests/

# Executar teste específico
python tests/teste_algo_crescimento.py
```

Testes cobrem:
- ✅ Detecção de crescimento uniforme
- ✅ Detecção de noise/falsos positivos
- ✅ Casos extremos (imagens vazias, muito pequenas)
- ✅ Comparação de imagens com dimensões diferentes

---

## 🐛 Troubleshooting

### Problema: "Nenhum resultado disponível"
**Solução:**
1. Verificar se pasta existe em `C:\Users\...\Documents`
2. Verificar nome da cidade em `data/coordenadas/`
3. Ver logs em `app.py` para detalhes

### Problema: Mapa não aparece
**Solução:**
1. Verificar se arquivo HTML foi gerado
2. Checar se coordenadas existem
3. Usar Flask em `http://localhost:5000` (não abrir HTML direto)

### Problema: Timelapse lento
**Solução:**
1. Reduzir número de imagens
2. Usar `--workers 8` para mais paralelização
3. Usar SSD em vez de HDD

### Problema: ImportError
**Solução:**
1. Ver [GUIA_IMPORTS.md](GUIA_IMPORTS.md)
2. Rodar: `python app/app.py` (não de outro lugar)
3. Checar se `src/` tem `__init__.py` em todas as pastas

---

## 📦 Dependências

```
rasterio>=1.3.0      # Leitura GeoTIFF
pillow>=9.0          # Processamento imagem
numpy>=1.20          # Cálculos
pandas>=1.3          # CSV/Dados
flask>=2.0           # Web
requests>=2.25       # HTTP
folium>=0.12         # Mapas
plotly>=5.0          # Gráficos
```

Instalar: `pip install -r requirements.txt`

---

## 📝 Licença

Projeto de pesquisa - Uso livre para fins educacionais e de análise.

---

## 👨‍💻 Desenvolvimento

### Estrutura de Imports (Novo)
Após reorganização, os módulos estão em subpastas. Use:

```python
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'processamento'))

from leitura_de_luz import AnalisadorLuzSatelite
```

Ver [GUIA_IMPORTS.md](GUIA_IMPORTS.md) para mais detalhes.

### Adicionar Novo Módulo
1. Criar arquivo em `src/` apropriado
2. Imports funcionam automaticamente se em `src/`
3. Testar: `python app/app.py`

### Deploy
```bash
# Usar gunicorn para produção
pip install gunicorn
gunicorn -b 0.0.0.0:5000 app.app:app
```

---

## 📊 Exemplos de Uso

### Exemplo 1: Processar Uma Cidade
```bash
python main.py
# Escolher opção 1, selecionar Brusque
```

### Exemplo 2: Gerar Mapa
```python
from mapa_crescimento import MapaCrescimento

mapa = MapaCrescimento()
mapa.gerar_relatorio_html_cidade('Brusque', 'mapa_brusque.html')
```

### Exemplo 3: Análise de Tendências
```python
from tendencias import AnalisadorTendencias

tendencia = AnalisadorTendencias()
resultado = tendencia.analisar_cidade('Brusque')
print(f"Taxa: {resultado['taxa_crescimento']}/ano")
```

---

## 🎯 Próximos Passos

✅ **Implementado:**
- Algoritmo de detecção de crescimento
- Interface web completa
- Mapas interativos e timelapses
- Análise de tendências
- Reorganização profissional

📝 **Ideias para Melhorias:**
- [ ] API REST para integração
- [ ] Dashboard com mais gráficos
- [ ] Exportar dados para GeoJSON
- [ ] Integração com banco de dados
- [ ] Previsões ML com LSTM

---

**Última atualização:** 2024  
**Status:** ✅ Pronto para uso  
**Suporte:** Ver `/docs` para guias e troubleshooting
