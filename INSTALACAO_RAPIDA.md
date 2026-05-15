# 📋 INSTALAÇÃO E CONFIGURAÇÃO RÁPIDA

## 1️⃣ Verificar Dependências

Abra PowerShell/Terminal e execute:

```bash
# Verificar Python
python --version

# Verificar se numpy, rasterio estão instalados
python -c "import numpy; import rasterio; import flask; print('✓ Dependências OK')"
```

## 2️⃣ Instalar Pacote de Automação (Opcional)

Se quiser automação automática:

```bash
pip install schedule
```

## 3️⃣ Começar a Usar

### Modo Interativo (Mais Fácil)

```bash
python main.py
```

Abre um menu com as 5 opções principais.

### Modo Direto (Command Line)

```bash
# Opção 1: Processar todas as imagens
python main.py 1

# Opção 2: Ver tendências
python main.py 2

# Opção 3: Configurar automação
python main.py 3

# Opção 4: Ver status
python main.py 4

# Opção 5: Limpar cache
python main.py 5
```

### Modo Direto (Scripts Individuais)

```bash
# Apenas processar
python processador_paralelo.py

# Apenas tendências
python tendencias.py

# Apenas automação
python automacao.py
```

---

## 🎯 Primeira Execução Passo a Passo

### PASSO 1: Processar Imagens
```bash
python main.py 1
```
⏱️ Espere 5-10 minutos...

### PASSO 2: Ver Resultados
```bash
python main.py 2
```
📊 Veja gráficos e tendências

### PASSO 3: (Opcional) Configurar Automação
```bash
python main.py 3
```
🤖 Configure para rodar automático

---

## 📁 Arquivos que Serão Criados

```
resultados.csv                    ← Dados de todas as imagens
processados.json                  ← Cache (não reprocessa)
automacao.log                     ← Log de automações
tendencia_10anos.png              ← Gráfico (10 anos)
comparacao_primeiro_ultimo.png    ← Gráfico (2015 vs 2024)
main.py                           ← Menu principal
processador_paralelo.py           ← Script de processamento
automacao.py                      ← Script de automação
tendencias.py                     ← Script de tendências
```

---

## 🐛 Se Algo Não Funcionar

### Erro: "Arquivo não encontrado"
```bash
# Verifique a pasta
ls "C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Bombinhas_recorte"

# Se não existir, edite processador_paralelo.py e altere:
pasta_base = Path(r"seu_caminho_aqui")
```

### Erro: "ModuleNotFoundError: No module named 'rasterio'"
```bash
# Reinstale
pip install --upgrade rasterio
```

### Arquivo resultados.csv vazio
```bash
# Execute novamente o processador
python main.py 1

# Veja os logs
# Abra: automacao.log
```

---

## ⚙️ Customização

### Adicionar Mais Cidades

Edite `processador_paralelo.py`:

```python
# ADICIONE isto ao final da classe ProcessadorParalelo:
# Mudança na função main() para processar múltiplas cidades

cidades = [
    r"C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Bombinhas_recorte",
    r"C:\Users\gtvargas\Documents\Outra_cidade\Raster\Recorte",
]

for cidade in cidades:
    proc = ProcessadorParalelo()
    proc.processar_pasta(cidade)
```

### Mudar Horário de Automação

Edite `automacao.py`:

```python
# Procura por:
# scheduler.add_job(processar, 'cron', hour=2, minute=0)

# Mude para:
# scheduler.add_job(processar, 'cron', hour=22, minute=30)  # 22:30
```

---

## 📊 Entender o CSV

### Formato
```
arquivo|ano|mes|intensidade_media|desvio_padrao|percentual_valido|threshold_crescimento|pixels_nulos|pixels_outliers
bombinhas_2015_01.tif|2015|1|82.45|15.30|97.3|90.12|1234|567
bombinhas_2015_02.tif|2015|2|84.20|16.10|96.8|92.35|1456|789
```

### Usar no Excel
1. Abrir resultados.csv no Excel
2. Dados → Tabela
3. Usar gráficos nativos
4. Salvar como .xlsx

---

## 🚀 Performance Esperada

| Ação | Tempo |
|------|-------|
| Processar 120 imagens | 5-10 min |
| Gerar tendências | <1 seg |
| Automação diária | Automático |
| Cache (reprocesso) | 0 seg |

---

## 📞 Suporte Rápido

**P: Onde estão os gráficos?**
R: Na mesma pasta que o script (procure .png)

**P: Como vejo o histórico?**
R: Abra resultados.csv no Excel

**P: Posso parar a automação?**
R: Task Scheduler → Desabilitar tarefa

**P: Como adiciono mais 2 cidades?**
R: Edite processador_paralelo.py e altere pasta_base

---

## ✅ Checklist de Instalação

- [ ] Python 3.7+ instalado
- [ ] numpy, rasterio, flask instalados
- [ ] Pasta de imagens acessível
- [ ] main.py na mesma pasta
- [ ] Executado `python main.py 1` com sucesso
- [ ] Visto resultados em resultados.csv
- [ ] (Opcional) Configurado automação

---

## 🎉 Pronto!

Agora você pode:
✅ Processar 1200+ imagens em paralelo (8-10x mais rápido)
✅ Ver tendências de 10 anos
✅ Automatizar processamento diário
✅ Tudo SEM banco de dados (apenas CSV)

Execute: `python main.py`
