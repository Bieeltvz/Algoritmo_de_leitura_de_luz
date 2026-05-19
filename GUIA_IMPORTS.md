# Guia de Imports - Após Reorganização

## 📁 Estrutura de Diretórios

```
projeto/
├── src/                          # 🔧 Código-fonte organizado
│   ├── processamento/            # Processamento de imagens
│   ├── mapas/                    # Geração de mapas
│   ├── analise/                  # Análises de dados
│   ├── utils/                    # Funções utilitárias
│   └── visualizacao/             # Visualização de dados
├── data/                         # 📊 Dados
│   ├── entrada/                  # Dados de entrada
│   ├── saida/                    # Resultados
│   ├── cache/                    # Cache processado
│   └── coordenadas/              # Coordenadas JSON
├── app/                          # 🌐 Interface web Flask
│   ├── app.py
│   ├── templates/
│   └── static/
├── docs/                         # 📚 Documentação
├── tests/                        # 🧪 Testes
├── outputs/                      # 📤 Arquivos gerados
├── main.py                       # 🚀 Entrada principal (CLI)
└── setup_path.py                 # 🔗 Configuração de paths
```

## 🔌 Como Usar os Novos Imports

### ✅ Forma Recomendada (após reorganização)

**Em main.py:**
```python
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'processamento'))
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'mapas'))
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'analise'))
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'utils'))
sys.path.insert(0, str(PROJECT_DIR / 'src'))

# Agora você pode fazer:
from leitura_de_luz import AnalisadorLuzSatelite
from processador_paralelo import ProcessadorParalelo
from mapa_crescimento import MapaCrescimento
from tendencias import AnalisadorTendencias
```

### 📍 Localização dos Módulos

| Módulo | Localização | Importar |
|--------|-----------|----------|
| `leitura_de_luz` | `src/processamento/` | `from leitura_de_luz import ...` |
| `processador_paralelo` | `src/processamento/` | `from processador_paralelo import ...` |
| `mapa_crescimento` | `src/mapas/` | `from mapa_crescimento import ...` |
| `heatmap_crescimento` | `src/mapas/` | `from heatmap_crescimento import ...` |
| `tendencias` | `src/analise/` | `from tendencias import ...` |
| `utils_*` | `src/utils/` | `from utils_* import ...` |

### 🚀 Executando o Projeto

```bash
# 1. CLI principal
python main.py

# 2. Interface web
python app/app.py

# 3. Em outro script Python
import sys
from pathlib import Path
PROJECT_DIR = Path(__file__).parent.parent  # Ajustar conforme localização
sys.path.insert(0, str(PROJECT_DIR / 'src' / 'processamento'))
# ... adicionar outros paths conforme necessário
from leitura_de_luz import AnalisadorLuzSatelite
```

## 🔄 Compatibilidade com Código Anterior

✅ **Mantido:** Todos os módulos estão nos mesmos arquivos Python
✅ **Compatível:** Code antigo continua funcionando com o sys.path setup
⚠️ **Nota:** Arquivos de teste/debug foram movidos para `tests/`

## 📦 Dependências Externas

Nenhuma mudança. Ainda usa:
- `rasterio` - GeoTIFF
- `pillow` - Imagens
- `numpy` - Arrays
- `pandas` - CSV/Dados
- `flask` - Web
- `requests` - HTTP

## ⚡ Quick Start

```bash
# Clonar ou usar estrutura existente
cd projeto

# 1. Interface web (recomendado)
python app/app.py
# Abrir http://localhost:5000

# 2. CLI
python main.py

# 3. Processar cidade específica
python main.py --processar Brusque
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'leitura_de_luz'"

✅ **Solução:** Verificar se:
1. Está em `src/processamento/`
2. Arquivo `__init__.py` existe em todas as pastas `src/`
3. main.py tem o setup correto de `sys.path`

### Erro: "FileNotFoundError" ao acessar dados

✅ **Verificar:** Paths em dados estão em `data/`
- Coordenadas: `data/coordenadas/coordenadas_cidades_completas_nominatim.json`
- Resultados: `data/saida/resultados_*.csv`

### Flask não encontra templates

✅ **Verificar:** `app/templates/` existe
Comando correto: `cd projeto` depois `python app/app.py`

## 📝 Notas

- Todos os `__init__.py` foram criados automaticamente
- `setup_path.py` pode ser usado como referência
- Cada pasta `src/` tem seu `__init__.py` para ser um package Python
- Não é necessário instalar os módulos, usar sys.path é suficiente

---

**Última atualização:** Reorganização de estrutura de projeto  
**Status:** ✅ Pronto para usar
