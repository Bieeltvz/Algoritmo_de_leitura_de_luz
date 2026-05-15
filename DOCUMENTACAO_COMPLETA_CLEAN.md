#  Sistema de Anlise de Luz Noturna via Satlite

## Documentao Completa das Funcionalidades

**Data:** Maio de 2026  
**Verso:** 2.0 Final  
**Tipo:** Aplicao Web + CLI para Processamento de Imagens de Satlite  

---

##  ndice

1. [Viso Geral](#viso-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Funcionalidades Principais](#funcionalidades-principais)
4. [Componentes Tcnicos](#componentes-tcnicos)
5. [APIs REST](#apis-rest)
6. [Interface Web](#interface-web)
7. [Processamento de Dados](#processamento-de-dados)
8. [Anlise e Relatrios](#anlise-e-relatrios)
9. [Automao](#automao)
10. [Guias de Uso](#guias-de-uso)

---

## Viso Geral

Este  um sistema completo de **anlise de iluminao noturna urbana** utilizando imagens de satlite TIFF (GeoTIFF). O sistema processa centenas de imagens de mltiplas cidades da regio do Vale do Itaja em Santa Catarina, detectando e analisando crescimento de luz ao longo de 10 anos (2014-2024).

### Caractersticas Principais

-  **Anlise de 1200+ imagens de satlite**
-  **Processamento paralelo de 8-10x mais rpido**
-  **Cobertura de 60+ cidades**
-  **Histrico de 10 anos (2014-2024)**
-  **Interface web moderna e responsiva**
-  **Deteco automtica de crescimento de luz**
-  **Gerao de grficos e tendncias**
-  **API REST completa**
-  **Sistema de cache inteligente**
-  **Automao por agendador de tarefas**
-  **Sugesto automtica de thresholds**
-  **Comparao peridica de imagens**

---

## Arquitetura do Sistema

```

                   Interface Web (Flask)                      
   app.py (Aplicao principal)                            
   templates/index.html (Interface responsiva)             
   static/ (CSS, JavaScript, assets)                       

                              

              Camada de Processamento                          
   leitura_de_luz.py (Anlise de intensidade)             
   processador_paralelo.py (Paralelo com threads)         
   tendencias.py (Anlise de tendncias)                  
   sugestores_threshold.py (Sugesto de limiares)         
   comparador_crescimento.py (Comparao de crescimento)   

                              

            Armazenamento de Dados                            
   resultados_*.csv (Dados processados)                   
   processados_*.json (Cache de imagens)                  
   coordenadas_*.json (Coordenadas de cidades)            

```

---

## Funcionalidades Principais

### 1.  Interface Web Interativa

Uma aplicao Flask moderna com Bootstrap 5 e Leaflet.js para visualizao geogrfica.

**Recursos:**
-  **Mapa interativo** das cidades com marcadores
-  **Seletor de cidades/recortes** por dropdown
-  **Visualizao de imagens** organizadas por ano
-  **Anlise individual de TIFF**
-  **Comparao entre perodos**
-  **Upload de arquivos personalizados**
-  **Painel de sugesto de thresholds**
-  **Recomendaes automticas**

**URL:** `http://localhost:5000`

---

### 2.  Processamento de Imagens TIFF

Anlise completa de imagens geoespaciais com deteco de anomalias.

#### Validaes Implementadas

**Deteco de Pixels Nulos:**
- Identifica pixels com valor 0 (erro do sensor)
- Detecta NaN (valores indefinidos)
- Diferencia entre erros reais e NoData legtimo (-9999)

**Deteco de Outliers:**
- Threshold fixo de 250 para intensidade luminosa
- Identifica anomalias do sensor
- Relatrio detalhado de qualidade

**Clculo de Estatsticas:**
- Mdia aritmtica de intensidade
- Mediana (valor central)
- Desvio padro (variao dos dados)
- Percentis (25%, 75%, etc)
- Intervalo Interquartil (IQR)

#### Mtricas Retornadas

```json
{
  "total_pixels": 250000,
  "pixels_validos": 248750,
  "percentual_valido": "99.50%",
  "intensidade_media": 45.32,
  "intensidade_mediana": 42.15,
  "intensidade_minima": 1.20,
  "intensidade_maxima": 248.95,
  "desvio_padrao": 28.45,
  "status": " ACEITA"
}
```

---

### 3.  Processamento Paralelo

Sistema de processamento multi-thread para velocidade 8-10x maior.

**Caractersticas:**
- Utiliza ThreadPoolExecutor com N workers
- Processa mltiplas imagens simultaneamente
- Sistema de cache inteligente (processados.json)
- Evita reprocessamento desnecessrio
- Progresso em tempo real

**Tempo de Processamento:**
- Sequencial: ~40 minutos (120 imagens)
- Paralelo: ~5-8 minutos (120 imagens)
- **Ganho: 500-800% mais rpido**

---

### 4.  Anlise de Tendncias

Gerao automtica de grficos e anlises estatsticas.

**Tipos de Anlise:**

#### Tendncia de 10 Anos
```
Grfico mostrando:
- Evoluo da intensidade mdia por ano
- Linha de tendncia (regresso linear)
- Intervalo de confiana
- Percentual de crescimento total
```

#### Comparao Primeiro vs ltimo
```
Grfico lado a lado:
- Primeira imagem do perodo (2014)
- ltima imagem do perodo (2024)
- Diferena de intensidade
- Percentual de mudana
```

#### Distribuio Estatstica
```
- Histograma de intensidades
- Caixa de distribuio (boxplot)
- Curva de densidade
```

---

### 5.  Sugesto de Thresholds

Anlise inteligente para sugerir valores de limiar para deteco de crescimento de luz.

**4 Nveis de Sugesto:**

1. **Conservador** -  Thresholds muito cautelosos
   - Detecta apenas crescimentos claros
   - Recomendado para anlises preliminares

2. **Moderado** -  Equilbrio entre sensibilidade e especificidade
   - Recomendado para anlises padro
   - Maioria dos casos de uso

3. **Agressivo** -  Alta sensibilidade
   - Detecta mudanas pequenas tambm
   - Recomendado para estudos detalhados

4. **Alto Crescimento** -  Apenas crescimentos significativos
   - Mxima sensibilidade
   - Deteco de anomalias extremas

**Cada sugesto inclui:**
- Valor do threshold em intensidade de luz
- Percentil estatstico correspondente
- Justificativa tcnica
- Recomendao baseada em contexto

---

### 6.  Comparao de Crescimento

Anlise comparativa entre duas imagens.

**Mtricas Calculadas:**
- Diferena de intensidade bruta
- Percentual de crescimento relativo
- Normalizao por varincia
- Status: CRESCIMENTO/DECRSCIMO/ESTVEL
- Significncia estatstica

**Exemplo:**
```
Comparao: 2014 vs 2024
 Intensidade 2014: 32.45
 Intensidade 2024: 47.82
 Crescimento: +15.37 (+47.3%)
 Status: CRESCIMENTO SIGNIFICATIVO
 Threshold: Excede 2.3 desvios padro
```

---

### 7.  Gerenciamento de Cidades

Suporte para 60+ cidades com descoberta automtica.

**Cidades Cobertas:**

*Costeiras:*
- Balnerio Cambori, Itaja, Itapema, Navegantes
- Penha, Porto Belo, Bombinhas, Barra Velha

*Vale Central:*
- Brusque, Gaspar, Blumenau, Pomerode
- Botuver, Guabiruba, Luiz Alves

*Alto Vale:*
- Indaial, Timb, Ibirama, Apina
- Rodeio, Rio dos Cedros, Blumenau

*Sudoeste/Sul:*
- Rio do Sul, Agrolandia, Atlanta
- Petrolndia, Aurora, Ituporanga

**Coordenadas Precisas:**
- Obtidas de IBGE (centroide oficial)
- Verificadas com Nominatim/OpenStreetMap
- Resoluo de ~50m

---

### 8.  Menu Principal (CLI)

Interface de linha de comando com 5 opes principais.

```
MENU PRINCIPAL
==============
1 - Processar todas as imagens
2 - Ver tendncias e grficos
3 - Configurar automao
4 - Ver status de processamento
5 - Limpar cache
```

---

## Componentes Tcnicos

### leitura_de_luz.py

**Classe: AnalisadorLuzSatelite**

Principal mecanismo de anlise de imagens.

```python
analisador = AnalisadorLuzSatelite(
    metodo_outlier='iqr',      # 'iqr' ou 'zscore'
    limiar_iqr=3.0,            # Sensibilidade IQR
    limiar_zscore=3.0,         # Sensibilidade Z-score
    modo_geoespacial=True      # Diferencia NoData
)

# Processar imagem
stats = analisador.processar_imagem(imagem_array)

# Comparar crescimento
comparacao = analisador.comparar_crescimento_luz(stats_ant, stats_atu)
```

**Mtodos Principais:**
- `processar_imagem()` - Anlise completa de uma imagem
- `comparar_crescimento_luz()` - Comparao entre imagens
- `gerar_relatorio()` - Formatao de relatrio
- `validar_pixels()` - Validao e limpeza de dados
- `detectar_outliers()` - Identificao de anomalias

---

### processador_paralelo.py

**Classe: ProcessadorParalelo**

Orquestrao de processamento multi-thread.

```python
processador = ProcessadorParalelo()
processador.processar_pasta(caminho)
```

**Otimizaes:**
- ThreadPoolExecutor com limite de workers
- Fila de tarefas gerenciada
- Progresso em tempo real
- Tratamento automtico de erros
- Retry para imagens problemticas

---

### tendencias.py

**Classe: AnalisadorTendencias**

Anlise estatstica e gerao de grficos.

```python
analisador = AnalisadorTendencias()
relatorio = analisador.gerar_relatorio(arquivo_csv)
```

**Relatrio Inclui:**
- Dados gerais (perodo, cidades)
- Anlise por ano
- Tendncia geral (regresso linear)
- Grficos PNG
- Recomendaes

---

### sugestores_threshold.py

**Classe: SugestorThreshold**

Sistema de sugesto inteligente de limiar.

```python
sugestor = SugestorThreshold()
sugestor.ler_csv('resultados_cidade.csv')
sugestor.calcular_stats_anuais()
sugestoes = sugestor.sugerir_thresholds()
```

**Retorna:**
```python
{
    'periodos': {'2014-2018': {...}, '2019-2024': {...}},
    'crescimento': {...},
    'thresholds_sugeridos': {
        'conservador': {...},
        'moderado': {...},
        'agressivo': {...},
        'alto_crescimento': {...}
    },
    'estatisticas_gerais': {...},
    'recomendacoes': [...]
}
```

---

### app.py

**Aplicao Flask Principal**

Servidor web com API REST completa.

**Configuraes:**
- HOST: localhost
- PORT: 5000
- MAX_UPLOAD: 50MB
- AUTO-DISCOVERY: Pastas de cidades

---

## APIs REST

### Endpoints Disponveis

#### 1. GET /
Pgina principal (HTML)

---

#### 2. GET /api/listar-imagens
Lista todas as imagens disponveis

**Resposta:**
```json
[
  {
    "ano": "2014",
    "imagens": [
      {
        "nome": "imagem_01.tif",
        "caminho": "/path/to/file",
        "tamanho_kb": 1024.5
      }
    ],
    "total": 12
  }
]
```

---

#### 3. POST /api/analisar
Analisa arquivo TIFF selecionado

**Request:**
```json
{
  "caminho": "/path/to/file.tif"
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "nome_arquivo": "imagem.tif",
  "dimensoes": "500  500",
  "total_pixels": "250,000",
  "pixels_validos": "248,750",
  "percentual_valido": "99.50%",
  "intensidade_media": "45.32",
  "intensidade_mediana": "42.15",
  "status": " ACEITA",
  "status_class": "success"
}
```

---

#### 4. POST /api/analisar-upload
Analisa arquivo TIFF enviado

**Request (multipart/form-data):**
- file: arquivo .tif/.tiff

**Resposta:** Mesma da anlise de arquivo

---

#### 5. POST /api/comparar-crescimento
Compara crescimento entre dois arquivos

**Request:**
```json
{
  "arquivo_anterior": "/path/1.tif",
  "arquivo_atual": "/path/2.tif"
}
```

**Resposta:**
```json
{
  "sucesso": true,
  "crescimento_media": 15.37,
  "percentual_crescimento": 47.3,
  "status_crescimento": "CRESCIMENTO",
  "crescimento_significativo": true,
  "detalhes": "..."
}
```

---

#### 6. GET /api/sugerir-thresholds
Sugesto de thresholds para cidade atual

**Resposta:**
```json
{
  "sucesso": true,
  "cidade": "Blumenau",
  "dados": {
    "periodos": {...},
    "crescimento": {...},
    "thresholds_sugeridos": {...},
    "recomendacoes": [...]
  }
}
```

---

#### 7. GET /api/pastas-cidades
Lista todas as cidades/recortes disponveis

**Resposta:**
```json
[
  {
    "id": "Blumenau_recorte",
    "nome_amigavel": "Blumenau - Recorte",
    "cidade": "Blumenau",
    "total_imagens": 145,
    "coordenadas": [-26.9196, -49.0658]
  }
]
```

---

#### 8. POST /api/selecionar-pasta
Seleciona a pasta de trabalho atual

**Request:**
```json
{
  "pasta": "Blumenau_recorte"
}
```

---

## Interface Web

### Componentes Principais

#### 1. Mapa Interativo
- **Biblioteca:** Leaflet.js 1.9.4
- **Provider:** OpenStreetMap
- **Zoom Padro:** 11
- **Centro:** Vale do Itaja (-27.079, -49.063)
- **Funcionalidade:** Clique em marcador = seleo de cidade

#### 2. Seletor de Cidades
- Dropdown com todas as cidades descobertas automaticamente
- Mostra nome amigvel e total de imagens
- Atualiza mapa ao selecionar

#### 3. Listagem de Imagens
- Organizadas por ano (2014-2024)
- Expandir/Recolher por ano
- Mostra tamanho em KB
- Boto de anlise por imagem

#### 4. Painel de Anlise Individual
- Exibio de todas as mtricas
- Status com cone colorido ( ACEITA,  VERIFICAR,  REJEITADA)
- Grfico visual de qualidade
- Boto para comparar com outra imagem

#### 5. Painel de Comparao
- Seletor de duas imagens
- Grfico de comparao lado a lado
- Anlise de crescimento
- Seta indicando crescimento ( acima,  abaixo,  estvel)

#### 6. Painel de Sugesto de Thresholds
-  Boto "Carregar Sugestes"
- 4 cards com sugestes coloridas
- Estatsticas gerais do perodo
- Tabela de anlise por ano
- Recomendaes listadas
- Exemplos de imagens de comparao (mximo, mnimo, mediano)
- Boto para exportar como CSV

#### 7. Seo de Upload
- rea drag-and-drop para TIFF
- Anlise automtica aps upload
- Suporta mltiplos formatos (.tif, .tiff)

---

### Tecnologias Frontend

- **Framework:** Bootstrap 5.3.0
- **Mapas:** Leaflet.js 1.9.4
- **cones:** Bootstrap Icons
- **JavaScript:** ES6 vanilla (sem jQuery)
- **Charts:** Plotly.js (via CDN)
- **Notificaes:** Bootstrap Toasts

---

## Processamento de Dados

### Fluxo de Dados

```
Pasta com Imagens TIFF
         
Descoberta Automtica (glob)
         
Fila de Processamento (ThreadPoolExecutor)
         
Anlise por Imagem (AnalisadorLuzSatelite)
     Validar dimenses
     Detectar pixels nulos
     Detectar outliers
     Calcular estatsticas
         
Cache em JSON (processados.json)
         
Salvar em CSV (resultados_*.csv)
```

### Formato de Dados

#### CSV Resultados
```
ano,mes,intensidade_media,intensidade_mediana,desvio_padrao,status
2014,1,32.45,31.20,12.50,ACEITA
2014,2,33.12,32.10,13.20,ACEITA
2014,3,34.89,33.95,14.10,ACEITA
```

#### JSON Cache
```json
{
  "2014/imagem_01.tif": {
    "intensidade_media": 32.45,
    "hash_processamento": "abc123...",
    "timestamp": 1609459200,
    "version": "2.0"
  }
}
```

---

## Anlise e Relatrios

### Relatrio Padro

Gerado para cada imagem:

```

           RELATRIO DE ANLISE DE INTENSIDADE DE LUZ          


 RESUMO DE VALIDAO:
   Total de pixels:        250,000
   Pixels vlidos:         248,750 (99.50%)
   Pixels nulos (erro):    1,200 (0.48%)
   Pixels outliers:        50 (0.02%)

 ESTATSTICAS DE INTENSIDADE (apenas pixels vlidos):
   Mdia:                    45.32
   Mediana:                  42.15
   Mnima:                   1.20
   Mxima:                  248.95
   Desvio padro:           28.45

 THRESHOLDS:
   Limite de outlier:       250.00
   Crescimento de luz:      59.53 (referncia p/ comparao)

 QUALIDADE DA IMAGEM:
   Status geral:  ACEITA
```

---

### Relatrio de Tendncias

Anlise anual com grficos:

```
ANLISE DE 10 ANOS (2014-2024)

Perodo: 2014-01 at 2024-12
Total de imagens: 145
Cidades analisadas: 1

ESTATSTICAS GERAIS:
 Intensidade mdia geral: 42.15
 Mxima anual: 47.89 (2024)
 Mnima anual: 32.45 (2014)
 Crescimento total: +15.44 (+47.6%)
 Tendncia: CRESCIMENTO LINEAR

CRESCIMENTO POR PERODO:
 2014-2018: +8.23 (+25.3%)
 2019-2022: +4.15 (+12.1%)
 2023-2024: +3.06 (+6.8%)

RECOMENDAES:
 Crescimento consistente indicando urbanizao
 Taxa de crescimento desacelerou em 2023-2024
```

---

## Automao

### Sistema de Agendamento

Integrao com Windows Task Scheduler para processamento automtico.

**Configurao:**
- **Frequncia:** Diria
- **Horrio:** 02:00 (2 AM)
- **Ao:** Processa imagens novas
- **Log:** automacao.log

**Arquivo: automacao.py**
```python
# Processa novas imagens todos os dias s 2 AM
schedule.every().day.at("02:00").do(processar)
```

---

## Guias de Uso

### 1. Instalao Rpida

```bash
# 1. Clonar/baixar o projeto
git clone <repositorio>
cd Algoritmo_de_leitura_de_luz

# 2. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependncias
pip install -r requirements.txt

# 4. Iniciar servidor
python app.py

# 5. Acessar em navegador
# http://localhost:5000
```

---

### 2. Primeiro Processamento

```bash
# Opo 1: Via Interface Web
# Selecionar cidade  Clicar em "Processar Todas as Imagens"

# Opo 2: Via CLI
python main.py 1
```

**Tempo esperado:** 5-10 minutos (120 imagens)

---

### 3. Anlise de Tendncias

```bash
# Via Interface Web
Clicar em " Tendncias" no menu

# Via CLI
python main.py 2
```

**Resultado:** Grficos PNG + Relatrio

---

### 4. Sugesto de Thresholds

```
Interface Web:
1. Selecionar cidade
2. Clicar em " Sugesto de Thresholds"
3. Clicar em "Carregar Sugestes"
4. Anlise automtica dos dados
5. 4 nveis de sugesto aparecem
```

---

### 5. Comparao de Duas Imagens

```
Interface Web:
1. Selecionar primeira imagem
2. Clicar em "Comparar"
3. Selecionar segunda imagem
4. Ver resultado de crescimento/decrscimo
```

---

### 6. Upload de Arquivo Personalizado

```
Interface Web:
1. Ir para seo "Upload de Arquivo TIFF"
2. Arrastar arquivo ou clicar para selecionar
3. Arquivo ser analisado automaticamente
```

---

### 7. Configurar Automao

```bash
# Via CLI
python main.py 3

# Seguir instrues na tela para criar tarefa agendada
```

---

## Estrutura de Diretrios

```
Algoritmo_de_leitura_de_luz/
 app.py                          # Aplicao Flask
 main.py                         # Menu principal
 leitura_de_luz.py              # Anlise de imagens
 processador_paralelo.py        # Processamento paralelo
 tendencias.py                  # Anlise de tendncias
 sugestores_threshold.py        # Sugesto de thresholds
 comparador_crescimento.py      # Comparao
 automacao.py                   # Agendamento automtico

 templates/
    index.html                 # Interface principal

 static/
    script.js                  # Lgica frontend
    style.css                  # Estilos
    assets/                    # Imagens/cones

 resultados_*.csv               # Dados processados
 processados_*.json             # Cache
 coordenadas_*.json             # Coordenadas

 docs/
     GUIA_RAPIDO.md
     INSTALACAO_RAPIDA.md
     INSTRUCOES_TESTE.md
     DOCUMENTACAO_COMPARACAO_IMAGENS.md
```

---

## Requisitos Tcnicos

### Dependncias Python

```
Flask>=2.0.0
numpy>=1.21.0
rasterio>=1.2.0
matplotlib>=3.4.0
Pillow>=8.0.0
schedule>=1.1.0
```

### Hardware Recomendado

- **CPU:** 4 cores (mnimo), 8 cores (recomendado)
- **RAM:** 8GB (mnimo), 16GB (recomendado)
- **Disco:** 10GB livres (dados + cache)
- **GPU:** No necessria

### Sistemas Operacionais

-  Windows 10/11
-  Linux (Ubuntu 18.04+)
-  macOS 10.15+

---

## Troubleshooting

### Problema: "Nenhuma pasta encontrada"
**Soluo:** Verificar se as imagens esto em `C:\Users\{usuario}\Documents\`

### Problema: "Erro ao analisar TIFF"
**Soluo:** Verificar se arquivo  GeoTIFF vlido com `gdalinfo`

### Problema: "Processamento muito lento"
**Soluo:** Verificar limite de threads, aumentar de 4 para 8

### Problema: "Porta 5000 j em uso"
**Soluo:** Executar em porta diferente: `python app.py --port 5001`

---

## Histrico de Verses

### v2.0 (Maio 2026) - ATUAL
-  Sugesto automtica de thresholds
-  Sistema de 4 nveis de sugesto
-  Exemplos de imagens variadas
-  Interface web melhorada
-  Documentao completa

### v1.5 (Maro 2026)
- Comparao de crescimento
- Anlise de tendncias
- Processamento paralelo

### v1.0 (Janeiro 2026)
- Anlise bsica de imagens
- Interface web inicial
- API REST

---

## Contato e Suporte

Para dvidas ou sugestes, consulte a documentao:
- GUIA_RAPIDO.md
- INSTALACAO_RAPIDA.md
- INSTRUCOES_TESTE.md

---

**Desenvolvido com  para anlise de crescimento urbano**
