# Algoritmo de Leitura de Luz - Estrutura do Projeto

Projeto de análise de crescimento de iluminação urbana usando imagens de satélite GeoTIFF.

## 📁 Estrutura de Pastas

```
Algoritmo_de_leitura_de_luz/
├── src/                          # Código-fonte principal
│   ├── processamento/            # Processamento de imagens e dados
│   │   ├── leitura_de_luz.py        # Core: leitura e processamento de imagens
│   │   ├── processador_paralelo.py  # Processamento paralelo de múltiplas cidades
│   │   ├── converter_csv.py         # Conversão de formatos de dados
│   │   ├── criar_csv.py             # Geração de arquivos CSV
│   │   └── processar_todas_cidades.py
│   │
│   ├── mapas/                    # Geração de mapas e visualizações
│   │   ├── mapa_crescimento.py      # Core: geração de mapas interativos
│   │   └── heatmap_crescimento.py   # Heatmaps de crescimento
│   │
│   ├── analise/                  # Análise de dados
│   │   ├── analise_valores.py       # Análise quantitativa
│   │   ├── diagnostico.py           # Diagnóstico de dados
│   │   ├── diagnostico_cidades.py
│   │   ├── diagnostico_resultados.py
│   │   └── tendencias.py            # Análise de tendências
│   │
│   ├── visualizacao/             # Visualizações (se necessário)
│   │
│   └── utils/                    # Utilidades e helpers
│       ├── atualizar_coordenadas_nominatim.py
│       ├── obter_coordenadas_ibge.py
│       ├── get_coordinates.py
│       └── validar_coordenadas.py
│
├── data/                         # Dados do projeto
│   ├── entrada/                  # Dados de entrada (se necessário)
│   ├── saida/                    # Dados processados
│   │   ├── resultados_*.csv         # Resultados de processamento
│   │   ├── processados_*.json       # Dados processados em JSON
│   │   └── *.geojson                # Dados geoespaciais
│   │
│   ├── cache/                    # Arquivos de cache
│   │
│   └── coordenadas/              # Arquivos de coordenadas
│       ├── coordenadas_cidades_completas_nominatim.json
│       ├── coordenadas_cidades_completas.json
│       ├── coordenadas_cidades_ibge.json
│       └── coordenadas_cidades_nominatim_preciso.json
│
├── docs/                         # Documentação
│   ├── GUIA_*.md
│   ├── DESCOBERTA_*.md
│   ├── DOCUMENTACAO_*.md
│   ├── INSTALACAO_*.md
│   ├── INSTRUCOES_*.md
│   ├── THRESHOLD_*.md
│   ├── RESUMO_*.md
│   ├── RELATORIO_*.md
│   └── SUMARIO_*.md
│
├── tests/                        # Testes
│   ├── test_*.py                    # Testes unitários
│   ├── debug_*.py                   # Scripts de debug (para investigação)
│   └── teste_*.py                   # Testes antigos
│
├── outputs/                      # Saídas geradas
│   ├── *.html                       # Timelapses e mapas interativos
│   ├── *.png                        # Imagens de heatmaps e visualizações
│   └── *.geojson                    # Dados geoespaciais
│
├── notebooks/                    # Jupyter Notebooks (se necessário)
│
├── app/                          # Aplicação Flask
│   ├── app.py                       # Aplicação web principal
│   ├── templates/                   # Templates HTML
│   └── static/                      # Arquivos estáticos (CSS, JS, etc)
│
├── requirements.txt              # Dependências do projeto
├── main.py                       # Script principal de entrada
└── README.md                     # Documentação original

```

## 🚀 Como Usar

### Instalação
```bash
pip install -r requirements.txt
```

### Executar a Aplicação Web
```bash
python app/app.py
```

### Executar Script Principal
```bash
python main.py
```

### Processar Todas as Cidades
```bash
python src/processamento/processar_todas_cidades.py
```

## 📊 Arquivos Principais

### Core (Processamento e Mapas)
- **`src/processamento/leitura_de_luz.py`** - Núcleo de processamento de imagens
- **`src/mapas/mapa_crescimento.py`** - Geração de mapas interativos
- **`src/mapas/heatmap_crescimento.py`** - Heatmaps de crescimento
- **`app/app.py`** - Interface web Flask

### Dados
- **`data/coordenadas/`** - Coordenadas geográficas de cidades
- **`data/saida/`** - Resultados de processamento (CSV e JSON)

### Documentação
- **`docs/`** - Toda a documentação em Markdown

## 🧪 Testes e Debug
- **`tests/`** - Todos os testes e scripts de debug
- Execute testes específicos conforme necessário

## 📤 Outputs
- **`outputs/`** - Timelapses HTML, mapas interativos e heatmaps PNG

## 🔧 Estrutura de Desenvolvimento

Siga a organização de pastas para manter o código limpo:

1. **src/** - Coloque todo o código reutilizável aqui
2. **data/** - Mantenha dados bem organizados por tipo
3. **docs/** - Adicione documentação em Markdown
4. **tests/** - Coloque testes e scripts de investigação
5. **outputs/** - Outputs são gerados automaticamente aqui

---
*Projeto organizado em 19/05/2026*
