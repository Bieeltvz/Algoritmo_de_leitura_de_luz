# 🌍 Descoberta Automática de Cidades - Atualização

## ✨ O que Mudou?

Agora o programa **descobre automaticamente todas as suas cidades** em `Documents` sem precisar de configuração manual!

---

## 🎯 Como Funciona

### Antes:
```
❌ Precisava editar app.py
❌ Configurar ALIAS_PASTAS manualmente
❌ Reiniciar para cada nova cidade
```

### Agora:
```
✅ Descobre automaticamente
✅ Nenhuma configuração necessária
✅ Novas cidades aparecem no dropdown
```

---

## 📁 Estrutura Esperada

O programa procura por este padrão em `Documents`:

```
C:\Users\gtvargas\Documents\
├── Bombinhas_noturno/                    ← Pasta com padrão "_noturno"
│   └── Raster/                           ← Pasta "Raster"
│       ├── Bombinhas_recorte/            ← Subpasta com padrão "_recorte"
│       │   ├── 2014/
│       │   │   ├── bombinhas_2014_01.tif
│       │   │   └── ...
│       │   ├── 2015/
│       │   └── ...
│       └── (outras subpastas _recorte)
│
├── Balneario_Picarras_noturno/           ← Outra cidade
│   └── Raster/
│       ├── Picarras_recorte/
│       │   ├── 2014/
│       │   └── ...
│       └── (outras subpastas _recorte)
│
└── (outras cidades com padrão _noturno)
```

---

## 🔍 Padrões Descobertos

O programa busca automaticamente:

1. **Pastas em Documents com sufixo `_noturno`**
   - `Bombinhas_noturno` ✅
   - `Balneario_Picarras_noturno` ✅
   - `Rio_de_Janeiro_noturno` ✅

2. **Dentro delas, pasta chamada `Raster`**
   - `Bombinhas_noturno/Raster/` ✅

3. **Dentro de Raster, subpastas com sufixo `_recorte`**
   - `Bombinhas_recorte` ✅
   - `Picarras_recorte` ✅
   - `Completo` ❌ (não tem sufixo _recorte)

---

## 📊 Exemplo de Seleção

Ao abrir http://localhost:5000, o dropdown mostra:

```
🏢 Bombinhas
   Recorte  (120 img)              ← Cidade (tipo_recorte) (contador)

🏢 Balneario Picarras              ← Outro exemplo
   Picarras  (180 img)

🏢 Rio De Janeiro
   Recorte  (150 img)
```

Clique em qualquer uma para alternar!

---

## ✅ Adicionar Novas Cidades

### Passo 1: Criar a estrutura
```
C:\Users\gtvargas\Documents\Sua_Cidade_noturno\
└── Raster\
    └── Sua_Recorte_recorte\
        ├── 2014\
        │   ├── imagem_2014_01.tif
        │   └── ...
        └── 2015\
            ├── imagem_2015_01.tif
            └── ...
```

### Passo 2: Reiniciar (apenas uma vez!)
```bash
python app.py
```

### Passo 3: Pronto! 
Sua cidade aparecerá no dropdown automaticamente.

---

## 🚀 API REST - Descoberta de Cidades

### Listar todas as cidades/pastas
```bash
curl http://localhost:5000/api/listar-pastas

# Retorna:
{
  "sucesso": true,
  "pastas": [
    {
      "nome": "Bombinhas_recorte",
      "nome_amigavel": "Bombinhas - Recorte",
      "cidade": "Bombinhas",
      "tipo_recorte": "Recorte",
      "total_imagens": 120,
      "selecionada": true
    },
    {
      "nome": "Picarras_recorte",
      "nome_amigavel": "Balneario Picarras - Picarras",
      "cidade": "Balneario Picarras",
      "tipo_recorte": "Picarras",
      "total_imagens": 180,
      "selecionada": false
    }
  ],
  "total_cidades": 2
}
```

---

## 📝 Mais Detalhes

### Nome Amigável Gerado Automaticamente

O programa extrai e formata os nomes:

```
Pasta: Bombinhas_noturno → Bombinhas
Tipo: Bombinhas_recorte  → Recorte
       ↓
Exibição: "Bombinhas - Recorte"
```

### Contador de Imagens

Automático! Conta `.tif` em todas as subpastas por ano:

```
Bombinhas_recorte/
├── 2014/  (30 .tif)
├── 2015/  (30 .tif)
└── 2016/  (30 .tif)
        ↓
Total: 120 imagens
```

---

## 🎯 Fluxo Técnico

```
App.py iniciado
    ↓
descobrir_pastas_cidades() chamado
    ↓
Procura em C:\Users\gtvargas\Documents
    ↓
Encontra pastas: *_noturno
    ↓
Dentro delas: procura Raster
    ↓
Dentro de Raster: procura *_recorte
    ↓
Monta PASTAS_DISPONIVEIS{} com todas encontradas
    ↓
Inicializa com primeira pasta
    ↓
Frontend carrega /api/listar-pastas
    ↓
Popula dropdown com todas as cidades
    ↓
Usuário clica em uma → muda instantaneamente
```

---

## 📊 Log de Inicialização

Veja no terminal ao executar `python app.py`:

```
2026-04-23 15:23:52,599 - INFO - Pasta inicial: Apiuna - Apiuna
```

Significa: `Descobriu e iniciou com Apiuna - Apiuna`

Se houver múltiplas:
```
INFO - Pasta inicial: Bombinhas - Recorte
INFO - Descobertas X cidades
```

---

## 🐛 Troubleshooting

### ❌ Problema: Nenhuma cidade aparece

**Causas possíveis:**
1. Pastas não seguem o padrão `*_noturno/Raster/*_recorte`
2. Nenhuma imagem `.tif` dentro
3. Documentos em caminho diferente

**Solução:**
```bash
# Verifique a estrutura:
ls C:\Users\gtvargas\Documents\ | findstr noturno
ls C:\Users\gtvargas\Documents\Bombinhas_noturno\Raster\ | findstr recorte
```

### ❌ Problema: Pasta não aparece no dropdown

**Verifique:**
1. Tem `_noturno` no final?
2. Tem pasta `Raster` dentro?
3. Tem `_recorte` nas subpastas?
4. Tem pelo menos um `.tif`?

Se tudo OK: `python app.py` novamente

---

## 🔄 Processamento em Lote

Funciona com descoberta automática!

```
1. Selecione uma cidade no dropdown
2. Clique "⚡ Lote"
3. Clique "Iniciar Processamento Paralelo"
4. Processa TODAS imagens da cidade selecionada
5. Salva em resultados.csv (específico da cidade)
```

---

## 📈 Tendências

Calcula baseado na pasta selecionada:

```
Seleciona: Bombinhas → Vê tendências de Bombinhas (2014-2024)
Seleciona: Picarras  → Vê tendências de Picarras (2014-2024)
Compara crescimento entre cidades!
```

---

## ✨ Conclusão

✅ **Automático** - Descobre todas as cidades  
✅ **Dinâmico** - Novas cidades aparecem sem restart  
✅ **Escalável** - Funciona com ilimitadas cidades  
✅ **Inteligente** - Conta imagens e formata nomes  

Basta manter a estrutura de pastas padrão!

```
Documentos/Cidade_noturno/Raster/Recorte_recorte/Anos/
```

🚀 **Pronto para usar!**
