# ⚡ Quick Start - Algoritmo de Leitura de Luz

## 🚀 3 Passos para Começar

### Passo 1: Instalar Dependências (1 min)
```bash
pip install -r requirements.txt
```

### Passo 2: Iniciar Interface Web (1 min)
```bash
python app/app.py
```

### Passo 3: Abrir no Navegador
Abrir: **http://localhost:5000** ✅

---

## 🎯 O Que Você Pode Fazer

✅ **Selecionar cidade** do Vale do Itajaí  
✅ **Gerar mapa interativo** com crescimento de luz  
✅ **Criar timelapse** animado (2013-2023)  
✅ **Ver percentual** de crescimento  
✅ **Visualizar heatmap** de intensidade  

---

## 📍 Dados Necessários

A aplicação funciona com:
- 📂 Imagens TIFF em `C:\Users\USUARIO\Documents\Nome_Cidade\`
- 📊 Coordenadas em `data/coordenadas/coordenadas_cidades_completas_nominatim.json`
- 📈 Resultados em `data/saida/resultados_*.csv`

**Exemplo:** `C:\Users\gtvargas\Documents\Brusque\` com imagens TIFF

---

## 🛠️ Alternativa: CLI (Menu)

Em vez de web, use menu:
```bash
python main.py
```

Menu com opções:
1. Processar imagens
2. Gerar timelapse
3. Gerar mapa
4. Analisar tendências

---

## 🐛 Problema?

1. **"Nenhum resultado"** → Verificar pasta em Documents
2. **Import error** → Ver [GUIA_IMPORTS.md](GUIA_IMPORTS.md)
3. **Porta 5000 em uso** → Mudar em `app/app.py` (linha com `app.run(port=5000)`)

---

## 📚 Leia Depois

- [README.md](README.md) - Guia completo
- [GUIA_INTERFACE_WEB.md](docs/GUIA_INTERFACE_WEB.md) - Como usar web
- [GUIA_RAPIDO.md](docs/GUIA_RAPIDO.md) - Mais detalhes (5 min)

---

**Pronto para começar? Execute: `python app/app.py`** ✨
