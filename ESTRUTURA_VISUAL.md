# 📦 Estrutura Final do Projeto

## Visualização Completa

```
Algoritmo_de_leitura_de_luz/
│
├── 📁 src/
│   ├── 📁 processamento/
│   │   ├── leitura_de_luz.py
│   │   ├── processador_paralelo.py
│   │   ├── converter_csv.py
│   │   ├── converter_csv_v2.py
│   │   ├── criar_csv.py
│   │   └── processar_todas_cidades.py
│   │
│   ├── 📁 mapas/
│   │   ├── mapa_crescimento.py
│   │   └── heatmap_crescimento.py
│   │
│   ├── 📁 analise/
│   │   ├── analise_valores.py
│   │   ├── diagnostico.py
│   │   ├── diagnostico_cidades.py
│   │   ├── diagnostico_resultados.py
│   │   └── tendencias.py
│   │
│   ├── 📁 utils/
│   │   ├── atualizar_coordenadas_nominatim.py
│   │   ├── obter_coordenadas_ibge.py
│   │   ├── get_coordinates.py
│   │   └── validar_coordenadas.py
│   │
│   └── 📁 visualizacao/
│       └── (vazio - para futuros gráficos)
│
├── 📁 data/
│   ├── 📁 entrada/
│   │   └── (vazio - para dados de entrada)
│   │
│   ├── 📁 saida/
│   │   ├── resultados_*.csv (59 arquivos)
│   │   ├── processados_*.json (26 arquivos)
│   │   └── *.geojson
│   │
│   ├── 📁 cache/
│   │   └── (vazio - para cache)
│   │
│   └── 📁 coordenadas/
│       ├── coordenadas_cidades_completas.json
│       ├── coordenadas_cidades_completas_nominatim.json
│       ├── coordenadas_cidades_ibge.json
│       └── coordenadas_cidades_nominatim_preciso.json
│
├── 📁 docs/
│   ├── GUIA_INTERFACE_WEB.md
│   ├── GUIA_PARALELO_SEM_BD.md
│   ├── GUIA_RAPIDO.md
│   ├── GUIA_SELECAO_PASTAS.md
│   ├── DESCOBERTA_AUTOMATICA_CIDADES.md
│   ├── DOCUMENTACAO_COMPARACAO_IMAGENS.md
│   ├── DOCUMENTACAO_COMPLETA_CLEAN.md
│   ├── INSTALACAO_RAPIDA.md
│   ├── INSTRUCOES_TESTE.md
│   ├── THRESHOLD_CRESCIMENTO_LUZ.md
│   ├── RESUMO_CORRECAO.txt
│   ├── RESUMO_DESCOBERTA_AUTO.md
│   ├── RESUMO_INTEGRACAO_WEB.md
│   ├── RESUMO_SELECAO_PASTAS.md
│   ├── RELATORIO_CORRECAO_COORDENADAS.md
│   ├── SUMARIO.md
│   ├── SUMARIO_DOCUMENTACAO.md
│   ├── SUMARIO_REORGANIZACAO.md
│   ├── README.md
│   ├── ALTERACOES.txt
│   └── (20+ arquivos de documentação)
│
├── 📁 tests/
│   ├── test_*.py (20 arquivos de teste)
│   ├── debug_*.py (15 arquivos de debug)
│   └── (41 arquivos total)
│
├── 📁 outputs/
│   ├── timelapse_*.html (15+ arquivos)
│   ├── mapa_*.html (5+ arquivos)
│   ├── heatmap_*.png (25+ arquivos)
│   ├── test_*.html
│   ├── test_*.png
│   └── (50 arquivos total)
│
├── 📁 notebooks/
│   └── (vazio - para Jupyter Notebooks)
│
├── 📁 app/
│   ├── app.py (aplicação Flask principal)
│   ├── 📁 templates/ (arquivos HTML)
│   └── 📁 static/ (CSS, JS, etc)
│
├── 📁 .git/
│   └── (controle de versão)
│
├── 📄 main.py (script principal)
├── 📄 requirements.txt (dependências)
├── 📄 README.md (documentação original)
└── 📄 README_ESTRUTURA.md (nova estrutura do projeto)

```

## 📊 Estatísticas

| Pasta | Arquivos | Descrição |
|-------|----------|-----------|
| `src/processamento` | 6 | Scripts de processamento de dados |
| `src/mapas` | 2 | Geração de mapas e heatmaps |
| `src/analise` | 5 | Análise de dados e diagnósticos |
| `src/utils` | 4 | Utilidades e helpers |
| `data/saida` | 80+ | Resultados e dados processados |
| `data/coordenadas` | 4 | Arquivos de coordenadas geográficas |
| `docs` | 22 | Documentação completa |
| `tests` | 41 | Testes e scripts de debug |
| `outputs` | 50 | Mapas, timelapses e gráficos gerados |
| **TOTAL** | **~270** | **Arquivos bem organizados** |

## 🎯 Principais Arquivos

### 🔴 Críticos (Não mova!)
- `src/processamento/leitura_de_luz.py` - Core do algoritmo
- `src/mapas/mapa_crescimento.py` - Geração de mapas
- `app/app.py` - Aplicação web
- `data/coordenadas/*.json` - Dados geográficos

### 🟡 Importantes
- `main.py` - Entrada principal
- `requirements.txt` - Dependências
- `docs/` - Toda documentação

### 🟢 Auxiliares
- `tests/` - Testes e debug
- `outputs/` - Saídas (regeneráveis)

## 🗑️ Arquivos Deletados

**Total: 42 arquivos removidos**

### PDFs e logs inuteis (8 arquivos)
- DOCUMENTACAO_COMPLETA.pdf
- DOCUMENTACAO_LEITURA_LUZ.pdf
- output.txt
- output_temp.txt
- debug_output.txt
- error.log
- README_DOCUMENTACAO.md
- .gitattributes

### Scripts de processamento específico (9 arquivos)
- processar_barra_velha.py
- processar_canelinha.py
- proc_balneario.py
- reprocessar_*.py (3 arquivos)
- find_canelinha.py
- find_missing_cities.py
- encontrar_barra.py

### Geradores de PDF (6 arquivos)
- gerar_pdf*.py (4 arquivos)
- convert_to_pdf.py
- check_original.py

### Utilidades antigas (13 arquivos)
- automacao.py
- limpar_cache.py
- sugestores_threshold.py
- verificar_*.py (3 arquivos)
- investigate_files.py
- listar_cidades_faltando.py
- coordenadas_corrigidas.py
- exemplos.py
- testes.py
- exemplo_crescimento_luz.py

## ✅ Benefícios

1. **Organização Clara** - Cada arquivo em seu lugar
2. **Fácil Manutenção** - Fácil localizar arquivos
3. **Sem Duplicação** - Removidos arquivos desnecessários
4. **Escalável** - Pronto para crescimento
5. **Profissional** - Segue padrões de projeto
6. **Melhor Performance** - Menos arquivo para procurar

---

*Última atualização: 19/05/2026*
