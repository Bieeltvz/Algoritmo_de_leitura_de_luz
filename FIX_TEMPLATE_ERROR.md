# ✅ RESOLVIDO: Aplicação Não Iniciava

## 🐛 Problema
```
jinja2.exceptions.TemplateNotFound: index.html
```

## 🔍 Causa Raiz
Flask procurava templates em `app/templates/` mas os arquivos estavam em:
- ❌ `templates/` (na raiz)
- ❌ `static/` (na raiz)

## ✅ Solução Aplicada

### 1. Movidos Templates
```
templates/               ❌
└── index.html

→ Movido para:

app/
├── templates/          ✅
│   └── index.html
└── static/             ✅
    ├── script.js
    └── style.css
```

### 2. Resolvido Problema de Encoding UTF-8
**Erro Original:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f310'
```

**Solução:**
```python
os.environ['PYTHONIOENCODING'] = 'utf-8'
```

### 3. Criados Scripts de Startup

#### `iniciar.bat` (Windows)
```batch
set PYTHONIOENCODING=utf-8
python app/app.py
```

#### `iniciar.py` (Multiplataforma)
```python
os.environ['PYTHONIOENCODING'] = 'utf-8'
subprocess.Popen([sys.executable, 'app.py'])
```

---

## 🚀 Como Usar Agora

### **Opção 1: Windows (Recomendado)**
```bash
# Clique duas vezes em:
iniciar.bat
```

### **Opção 2: Multiplataforma**
```bash
python iniciar.py
```

### **Opção 3: Terminal Manual**
```bash
$env:PYTHONIOENCODING='utf-8'
python app/app.py
```

---

## ✅ Verificação

Abrir: **http://localhost:5000**

Você deve ver:
- ✅ Página carregando
- ✅ Mapa com 56 cidades
- ✅ Interface responsiva
- ✅ Botões funcionando

---

## 📁 Estrutura Final (Corrigida)

```
Algoritmo_de_leitura_de_luz/
├── app/                       ← Flask app
│   ├── app.py                ✅ Servidor
│   ├── templates/            ✅ HTML (MOVIDO)
│   │   └── index.html
│   └── static/               ✅ CSS/JS (MOVIDO)
│       ├── script.js
│       └── style.css
│
├── iniciar.bat               ✅ NOVO - Windows
├── iniciar.py                ✅ NOVO - Python
├── COMO_INICIAR.md           ✅ NOVO - Guia
│
├── src/                      ← Código-fonte
├── data/                     ← Dados
├── docs/                     ← Documentação
└── ...
```

---

## 🎉 Status

✅ **Aplicação iniciando corretamente**  
✅ **Templates encontrados**  
✅ **Encoding UTF-8 funcionando**  
✅ **Pronto para usar**

---

**Data:** 19/05/2026  
**Problema:** TemplateNotFound  
**Status:** ✅ RESOLVIDO
