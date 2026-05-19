# 📁 Guia de Seleção de Pastas - Análise de Luz Noturna

## 🎯 O que é a Seleção de Pastas?

Agora você pode **selecionar diferentes pastas de imagens** diretamente na interface web sem precisar reiniciar a aplicação. Perfeito para analisar múltiplas cidades ou regiões!

---

## 🚀 Como Usar

### 1️⃣ **Acessar o Dropdown de Pastas**
- Abra a aplicação: **http://localhost:5000**
- Veja o dropdown na navbar: **🖼️ Bombinhas_recorte**
- Clique para ver todas as pastas disponíveis

### 2️⃣ **Selecionar uma Pasta**
```
Clique em uma pasta → A pasta é alterada → Volte à análise
```

### 3️⃣ **Começar Análise**
- Todos os recursos funcionam com a pasta selecionada:
  - 🖼️ **Individual**: Analisa imagens da pasta selecionada
  - ⚡ **Lote**: Processa todas as imagens da pasta selecionada
  - 📊 **Tendências**: Calcula baseado na pasta selecionada

---

## 📝 Configurar Suas Próprias Pastas

### Estrutura de Pastas Esperada
```
C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\
├── Bombinhas_recorte/          ← Pasta 1
│   ├── 2015/
│   │   ├── bombinhas_2015_01.tif
│   │   ├── bombinhas_2015_02.tif
│   │   └── ...
│   ├── 2016/
│   └── ...
├── Bombinhas/                  ← Pasta 2 (completo)
│   ├── 2015/
│   └── ...
├── Rio_de_Janeiro/             ← Pasta 3
│   ├── 2015/
│   └── ...
└── Sao_Paulo/                  ← Pasta 4
    ├── 2015/
    └── ...
```

### Como Adicionar uma Pasta

**Passo 1:** Crie a pasta com suas imagens
```
C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Sua_Cidade\
```

**Passo 2:** Organize por anos
```
Sua_Cidade/
├── 2015/
│   ├── imagem_2015_01.tif
│   ├── imagem_2015_02.tif
└── 2016/
    ├── imagem_2016_01.tif
```

**Passo 3:** Adicione alias (nome amigável) em `app.py`
```python
ALIAS_PASTAS = {
    'Bombinhas_recorte': 'Bombinhas (Recorte)',
    'Bombinhas': 'Bombinhas (Completo)',
    'Rio_de_Janeiro': 'Rio de Janeiro',      # ← Novo
    'Sua_Cidade': 'Minha Cidade Legal',      # ← Novo
}
```

**Passo 4:** Reinicie a aplicação
```bash
python app.py
```

**Pronto!** Sua pasta aparecerá no dropdown com o nome amigável.

---

## 🔧 Configuração Avançada

### Alterar Pasta Raiz Padrão

Se suas pastas estão em outro local, edite em `app.py`:

```python
# ANTES:
CAMINHO_RAIZ = Path(r"C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster")

# DEPOIS:
CAMINHO_RAIZ = Path(r"D:\Meus Dados\Imagens Satélite")
```

### Alterar Pasta Selecionada por Padrão

Se quer que outra pasta seja o padrão inicial:

```python
# ANTES:
PASTA_SELECIONADA = {
    'caminho': Path(r"C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Bombinhas_recorte"),
    'nome': 'Bombinhas_recorte'
}

# DEPOIS:
PASTA_SELECIONADA = {
    'caminho': Path(r"C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Rio_de_Janeiro"),
    'nome': 'Rio_de_Janeiro'
}
```

---

## 📊 APIs Disponíveis

Se você quiser integrar com outro sistema, temos APIs REST:

### 1️⃣ Listar Pastas Disponíveis
```bash
curl http://localhost:5000/api/listar-pastas
```

**Resposta:**
```json
{
  "sucesso": true,
  "pastas": [
    {
      "nome": "Bombinhas_recorte",
      "nome_amigavel": "Bombinhas (Recorte)",
      "caminho": "C:\\Users\\...\\Bombinhas_recorte",
      "total_imagens": 120,
      "selecionada": true
    }
  ],
  "pasta_atual": "Bombinhas_recorte"
}
```

### 2️⃣ Selecionar Pasta
```bash
curl -X POST http://localhost:5000/api/selecionar-pasta \
  -H "Content-Type: application/json" \
  -d '{"nome_pasta": "Rio_de_Janeiro"}'
```

**Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Pasta selecionada: Rio de Janeiro",
  "pasta_atual": "Rio_de_Janeiro",
  "nome_amigavel": "Rio de Janeiro"
}
```

### 3️⃣ Obter Pasta Atual
```bash
curl http://localhost:5000/api/pasta-atual
```

**Resposta:**
```json
{
  "sucesso": true,
  "nome": "Bombinhas_recorte",
  "nome_amigavel": "Bombinhas (Recorte)",
  "caminho": "C:\\Users\\...\\Bombinhas_recorte"
}
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Analisar Múltiplas Cidades em Lote

```
1. Acesse http://localhost:5000
2. Selecione "Rio de Janeiro" no dropdown
3. Clique ⚡ Lote → "Iniciar Processamento Paralelo"
4. Espere 5-10 minutos
5. Veja resultados com todos os dados de Rio de Janeiro
6. Selecione "São Paulo"
7. Processe novamente
8. Repita para outras cidades
```

### Exemplo 2: Comparar Crescimento Entre Cidades

```
1. Selecione Bombinhas
2. Veja tendência: média 90.58 (2015-2024)
3. Anote o valor final
4. Selecione Rio_de_Janeiro
5. Veja tendência: compare com Bombinhas
6. Identifique qual teve maior crescimento
```

### Exemplo 3: Análise Individual de Imagem Específica

```
1. Selecione pasta (ex: Bombinhas)
2. Clique 🖼️ Individual
3. Selecione imagem do dropdown (ex: bombinhas_2024_01.tif)
4. Veja estatísticas completas
5. Mude pasta se quiser comparar com outra cidade
```

---

## 🐛 Troubleshooting

### ❌ Problema: Pasta não aparece no dropdown

**Solução:**
1. Verifique que a pasta está em: `C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\`
2. Verifique que a pasta tem imagens em subpastas por ano:
   ```
   Sua_Pasta/
   ├── 2015/
   │   └── arquivo.tif
   ```
3. Reinicie a aplicação: `python app.py`

### ❌ Problema: Mudei pasta mas ainda vê dados antigos

**Solução:**
1. Limpe o cache de resultados:
   ```bash
   del resultados.csv
   del processados.json
   ```
2. Selecione a pasta novamente
3. Clique "Iniciar Processamento Paralelo"

### ❌ Problema: Pasta não encontrada em app.py

**Solução:**
1. Edite `app.py` e corrija o `CAMINHO_RAIZ`
2. Certifique-se de usar aspas duplas e barras invertidas:
   ```python
   CAMINHO_RAIZ = Path(r"C:\Caminho\Correto")  # ✅ Correto
   ```

---

## ✨ Recursos

- ✅ Seleção visual no dropdown da navbar
- ✅ Contador de imagens por pasta
- ✅ Checkmark para pasta selecionada
- ✅ Notificação ao mudar pasta
- ✅ Toda análise respeita pasta selecionada
- ✅ API REST para integração

---

## 🎉 Próximos Passos

1. **Configure suas cidades** em `ALIAS_PASTAS`
2. **Adicione mais pastas** seguindo a estrutura
3. **Use o dropdown** para alternar entre elas
4. **Processe em lote** cada pasta quando quiser

Qualquer dúvida, consulte o terminal (logs) ou os comentários no código! 🚀
