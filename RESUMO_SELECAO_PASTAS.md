# 📋 Resumo - Seleção de Pastas Adicionada

## ✨ O que foi Adicionado

### 🔧 **Backend (app.py)**

**Variáveis Globais Novas:**
```python
CAMINHO_RAIZ = Path(r"C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster")
PASTA_SELECIONADA = {'caminho': ..., 'nome': 'Bombinhas_recorte'}
ALIAS_PASTAS = {'Bombinhas_recorte': 'Bombinhas (Recorte)', ...}
```

**3 Novas Rotas API:**
- `GET /api/listar-pastas` - Lista todas as pastas com contador de imagens
- `POST /api/selecionar-pasta` - Muda a pasta ativa
- `GET /api/pasta-atual` - Retorna pasta selecionada

**Funções Atualizadas:**
- `listar_imagens()` - Usa `PASTA_SELECIONADA['caminho']`
- `api_processar_paralelo()` - Processa pasta selecionada (não mais hardcoded)

---

### 🎨 **Frontend (index.html)**

**Novo Dropdown na Navbar:**
```html
<!-- Botão de seleção de pasta com lista de pastas disponíveis -->
<div class="dropdown">
    <button class="btn btn-sm btn-outline-light dropdown-toggle" 
            id="dropdownPastas" data-bs-toggle="dropdown">
        🖼️ <span id="pasta-atual-nome">Carregando...</span>
    </button>
    <ul class="dropdown-menu dropdown-menu-end" id="lista-pastas">
        <!-- Pastas preenchidas dinamicamente -->
    </ul>
</div>
```

---

### ⚙️ **JavaScript (script.js)**

**3 Novas Funções:**

1. **`carregarPastasDisponiveis()`**
   - Chama `/api/listar-pastas`
   - Popula dropdown com pastas disponíveis
   - Mostra contador de imagens
   - Indica pasta selecionada com checkmark

2. **`selecionarPasta(nomePasta)`**
   - Chama `/api/selecionar-pasta` (POST)
   - Atualiza navbar com nome da pasta
   - Mostra notificação de sucesso/erro
   - Recarrega lista de pastas

3. **`mostrarNotificacao(mensagem, tipo)`**
   - Exibe alerta temporário (3 segundos)
   - Tipos: success, danger, info, warning
   - Usa `position-fixed` para ficar visível

**DOMContentLoaded:**
- Agora chama `carregarPastasDisponiveis()` ao carregar a página

---

### 🎨 **CSS (style.css)**

**Estilos Novos:**
```css
/* Dropdown de Pastas */
#dropdownPastas - Botão com hover/scale
.dropdown-menu - Menu com sombra e border-radius
.dropdown-item - Item com flexbox, hover e espaçamento
```

---

## 🎯 Como Usar

### Interface Visual
1. **Acesse:** http://localhost:5000
2. **Veja:** Dropdown na navbar superior direita
3. **Clique:** Selecione uma pasta
4. **Pronto:** Todos os recursos usam a pasta selecionada

### Adicionar Novas Pastas
1. Crie a estrutura:
   ```
   C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Nova_Cidade\
   ├── 2015/
   │   └── arquivo.tif
   └── 2016/
       └── arquivo.tif
   ```

2. Edite `app.py` - adicione à `ALIAS_PASTAS`:
   ```python
   'Nova_Cidade': 'Nome Amigável'
   ```

3. Reinicie: `python app.py`

---

## 📊 APIs Disponíveis

### Listar Pastas
```bash
GET /api/listar-pastas

# Retorna:
{
  "sucesso": true,
  "pastas": [
    {
      "nome": "Bombinhas_recorte",
      "nome_amigavel": "Bombinhas (Recorte)",
      "total_imagens": 120,
      "selecionada": true
    }
  ]
}
```

### Selecionar Pasta
```bash
POST /api/selecionar-pasta
Content-Type: application/json

{"nome_pasta": "Rio_de_Janeiro"}

# Retorna:
{
  "sucesso": true,
  "mensagem": "Pasta selecionada: Rio de Janeiro",
  "pasta_atual": "Rio_de_Janeiro"
}
```

### Pasta Atual
```bash
GET /api/pasta-atual

# Retorna:
{
  "sucesso": true,
  "nome": "Bombinhas_recorte",
  "nome_amigavel": "Bombinhas (Recorte)",
  "caminho": "C:\\Users\\...\\Bombinhas_recorte"
}
```

---

## 🔄 Fluxo Técnico

```
Página carrega
    ↓
DOMContentLoaded dispara
    ↓
carregarPastasDisponiveis() chamado
    ↓
GET /api/listar-pastas
    ↓
Frontend popula dropdown
    ↓
Usuário clica em uma pasta
    ↓
selecionarPasta(nome) chamado
    ↓
POST /api/selecionar-pasta
    ↓
Backend atualiza PASTA_SELECIONADA global
    ↓
Frontend mostra notificação
    ↓
Todos recursos usam nova pasta
```

---

## 🎯 Integração com Recursos Existentes

Todos os recursos já funcionam com a seleção:

✅ **Análise Individual**
- Seleciona pasta → Imagens da pasta aparecem no dropdown

✅ **Comparação de Crescimento**
- Ambas imagens precisam estar na pasta selecionada

✅ **Processamento em Lote**
- Processa TODAS as imagens da pasta selecionada

✅ **Tendências**
- Calcula baseado no CSV da pasta selecionada

✅ **Status de Processamento**
- Mostra status da pasta atual

---

## 📁 Arquivos Modificados

| Arquivo | Mudanças |
|---------|----------|
| `app.py` | 3 novas rotas, variáveis globais, atualização de funções |
| `templates/index.html` | Dropdown na navbar |
| `static/script.js` | 3 novas funções + DOMContentLoaded atualizado |
| `static/style.css` | Estilos para dropdown e notificações |

---

## 📁 Novo Arquivo

| Arquivo | Descrição |
|---------|-----------|
| `GUIA_SELECAO_PASTAS.md` | Guia completo de configuração e uso |

---

## ✅ Checklist

- [x] Backend: 3 rotas API criadas
- [x] Frontend: Dropdown adicionado à navbar
- [x] JavaScript: Funções de gerenciamento de pastas
- [x] CSS: Estilos para dropdown e notificações
- [x] Documentação: Guia completo criado
- [x] Teste: App.py rodando sem erros
- [x] Integração: Todos recursos usam pasta selecionada

---

## 🚀 Próximo Passo

```bash
# Terminal 1: Rodando
python app.py

# Terminal 2 (nova aba): Testar a API
curl http://localhost:5000/api/listar-pastas
```

Acesse: **http://localhost:5000**

Veja o dropdown de pastas na navbar e teste alternar entre pastas! 🎉
