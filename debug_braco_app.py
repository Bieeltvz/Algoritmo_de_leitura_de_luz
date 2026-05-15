#!/usr/bin/env python3
"""
Debug: Testar exatamente o que app.py está fazendo para Braco Do Trombudo
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("=== Simulando o que app.py faz ===\n")

# Simular o que descobrir_pastas_cidades faz
CAMINHO_DOCUMENTOS = Path(r"C:\Users\gtvargas\Documents")
print(f"Procurando em: {CAMINHO_DOCUMENTOS}")

if not CAMINHO_DOCUMENTOS.exists():
    print("❌ Documents não encontrado")
else:
    print("✅ Documents existe")
    
    # Procurar por "Braco_Do_Trombudo" em subpastas
    print("\nProcurando por pastas com 'Braco':")
    encontradas = []
    
    for item in CAMINHO_DOCUMENTOS.rglob("*Braco*"):
        if item.is_dir():
            print(f"  Pasta: {item.relative_to(CAMINHO_DOCUMENTOS)}")
            encontradas.append(item)
            
            # Contar imagens TIF
            tif_count = len(list(item.glob("**/*.tif")))
            print(f"    Imagens TIF: {tif_count}")
    
    if not encontradas:
        print("  ❌ Nenhuma pasta encontrada")

print("\n" + "="*60 + "\n")

# Agora testar o MapaCrescimento
print("Testando MapaCrescimento:")

m = MapaCrescimento()
m.carregar_coordenadas()

# Teste 1: calcular_crescimento_cidade_unica
print("\n1. Testando calcular_crescimento_cidade_unica('Braco_Do_Trombudo'):")
resultado = m.calcular_crescimento_cidade_unica('Braco_Do_Trombudo')
if resultado:
    print(f"   ✅ Sucesso: {resultado}")
else:
    print(f"   ❌ Falhou")

# Teste 2: encontrar CSV
print("\n2. Testando encontrar_arquivo_csv('Braco_Do_Trombudo'):")
csv = m.encontrar_arquivo_csv('Braco_Do_Trombudo')
if csv:
    print(f"   ✅ CSV encontrado: {csv}")
else:
    print(f"   ❌ CSV não encontrado")

# Teste 3: Verificar se a pasta existe
print("\n3. Verificando pasta da cidade:")
pasta_base = Path(__file__).parent.absolute()
print(f"   Base: {pasta_base}")

# Procurar por padrões como app.py faz
print("\n4. Procurando pelo padrão de descoberta do app.py:")
for subpasta in pasta_base.glob("*"):
    if subpasta.is_dir() and "braco" in subpasta.name.lower():
        print(f"   Encontrada: {subpasta.name}")
        tif_files = len(list(subpasta.glob("**/*.tif")))
        print(f"   Imagens TIF: {tif_files}")

print("\n" + "="*60)
print("\n⚠️ Verificando: O app.py procura em C:\\Users\\gtvargas\\Documents")
print("   Mas as imagens podem estar em outra pasta!")
