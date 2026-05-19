#!/usr/bin/env python3
"""
Debug: Tentar gerar timelapse para Braco_Do_Trombudo
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

print("=== Gerando timelapse para Braco_Do_Trombudo ===\n")

m = MapaCrescimento()
m.carregar_coordenadas()

# Dados da cidade
nome_cidade = 'Braco_Do_Trombudo'
nome_amigavel = 'Braco Do Trombudo - Braco Do Trombudos'

print(f"Cidade: {nome_amigavel}")

# Procurar pasta com imagens
CAMINHO_DOCUMENTOS = Path(r"C:\Users\gtvargas\Documents")

pasta_encontrada = None
for item in CAMINHO_DOCUMENTOS.rglob("*Braco*Do*Trombudo*"):
    if item.is_dir():
        # Contar TIF
        tif_count = len(list(item.glob("**/*.tif")))
        if tif_count > 0:
            print(f"✅ Pasta encontrada: {item}")
            print(f"   Imagens TIF: {tif_count}")
            pasta_encontrada = item
            break

if not pasta_encontrada:
    print("❌ Pasta não encontrada em Documents")
    print("\nProcurando no diretório local:")
    
    for item in Path(__file__).parent.absolute().glob("*Braco*"):
        if item.is_dir():
            tif_count = len(list(item.glob("**/*.tif")))
            print(f"  {item.name}: {tif_count} imagens TIF")

else:
    print(f"\n📁 Processando pasta: {pasta_encontrada}")
    
    try:
        arquivo_saida = Path(__file__).parent.absolute() / f'timelapse_{nome_cidade}_debug.html'
        
        print(f"📝 Arquivo de saída: {arquivo_saida}")
        print("\n⏳ Gerando timelapse...")
        
        resultado = m.gerar_timelapse_cidade(
            nome_cidade,
            str(pasta_encontrada),
            str(arquivo_saida)
        )
        
        if resultado:
            print(f"✅ Timelapse gerado com sucesso!")
            if Path(arquivo_saida).exists():
                tamanho_mb = Path(arquivo_saida).stat().st_size / (1024*1024)
                print(f"   Arquivo: {arquivo_saida}")
                print(f"   Tamanho: {tamanho_mb:.1f} MB")
        else:
            print(f"❌ Falha ao gerar timelapse")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
