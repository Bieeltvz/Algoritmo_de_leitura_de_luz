# ✅ Como Iniciar a Aplicação

## 🚀 3 Formas para Iniciar

### Forma 1: Script Batch (Windows) ⭐ Recomendado

```bash
# No Windows, execute:
iniciar.bat
```

Ou clique duas vezes no arquivo `iniciar.bat`

**O que faz:**
- Configura encoding UTF-8
- Inicia o Flask
- Abre na porta 5000

### Forma 2: Script Python

```bash
python iniciar.py
```

**O que faz:**
- Verifica arquivos necessários
- Configura paths automáticamente
- Inicia Flask

### Forma 3: Manual (Terminal)

```bash
# De qualquer lugar, configure encoding e rode:
$env:PYTHONIOENCODING='utf-8'
python app/app.py
```

---

## ✅ Depois de Iniciar

**Abra o navegador:**
```
http://localhost:5000
```

Você verá:
- 🌍 Mapa com todas as cidades
- 📍 Clique em uma cidade
- 🎬 Gere timelapse
- 🗺️ Gere mapa interativo

---

## 🐛 Se Houver Erro

### "TemplateNotFound"
✅ **RESOLVIDO** - Templates foram movidos para `app/templates/`

### "UnicodeEncodeError" 
✅ **RESOLVIDO** - Use `iniciar.bat` ou `iniciar.py`

### "ModuleNotFoundError"
Verifique que está em: `Algoritmo_de_leitura_de_luz/`

---

## 📊 Estrutura Corrigida

```
Algoritmo_de_leitura_de_luz/
├── app/
│   ├── app.py              ← Servidor Flask
│   ├── templates/          ← HTML (agora aqui!)
│   │   └── index.html
│   └── static/             ← CSS, JS (agora aqui!)
│       ├── script.js
│       └── style.css
├── iniciar.bat             ← Windows (recomendado)
├── iniciar.py              ← Python
└── ...
```

---

**Pronto! Clique em `iniciar.bat` e aproveite! 🎉**
