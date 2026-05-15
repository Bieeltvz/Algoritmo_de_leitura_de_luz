#!/usr/bin/env python3
"""
Teste: Simular exactamente o que app.py faz quando gera timelapse
"""

from pathlib import Path
from mapa_crescimento import MapaCrescimento
import logging
import sys

# Configurar encoding para UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

print("=== Simulando app.py gerar_timelapse ===\n")

# Dados que viriam de PASTA_SELECIONADA no app.py
teste_cidades = [
    {'nome': 'Braco_Do_Trombudo', 'amigavel': 'Braco Do Trombudo - Braco Do Trombudos'},
    {'nome': 'Bombinhas_recorte', 'amigavel': 'Bombinhas - Recorte'},
    {'nome': 'Picarras_recorte', 'amigavel': 'Picarras - Recorte'},
]

DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
CAMINHO_DOCUMENTOS = Path(r"C:\Users\gtvargas\Documents")

m = MapaCrescimento()
m.carregar_coordenadas()

for teste in teste_cidades:
    nome_cidade = teste['nome']
    nome_amigavel = teste['amigavel']
    
    print(f"\nTestando: {nome_amigavel}")
    print("=" * 60)
    
    # Procurar pasta
    pasta_encontrada = None
    
    # Tentar em Documents (como faria app.py)
    if CAMINHO_DOCUMENTOS.exists():
        for item in CAMINHO_DOCUMENTOS.rglob(f"*{nome_cidade.split('_')[0]}*"):
            if item.is_dir() and any(f in item.name for f in nome_cidade.split('_')):
                tif_count = len(list(item.glob("**/*.tif")))
                if tif_count > 0:
                    pasta_encontrada = item
                    print(f"  Pasta em Documents: {item.name}")
                    print(f"  Imagens TIF: {tif_count}")
                    break
    
    # Fallback: procurar no diretório local
    if not pasta_encontrada:
        for item in DIRETORIO_TRABALHO.glob(f"*{nome_cidade}*"):
            if item.is_dir():
                tif_count = len(list(item.glob("**/*.tif")))
                if tif_count > 0:
                    pasta_encontrada = item
                    print(f"  Pasta local: {item.name}")
                    print(f"  Imagens TIF: {tif_count}")
                    break
    
    if pasta_encontrada:
        try:
            # Simular o que app.py faz
            arquivo_html = DIRETORIO_TRABALHO / f'timelapse_{nome_cidade}.html'
            print(f"  Gerando: {arquivo_html.name}")
            
            arquivo_gerado = m.gerar_timelapse_cidade(
                nome_cidade,
                str(pasta_encontrada),
                str(arquivo_html)
            )
            
            if arquivo_gerado and arquivo_html.exists():
                tamanho_mb = arquivo_html.stat().st_size / (1024*1024)
                print(f"  SUCESSO: {tamanho_mb:.1f} MB")
            else:
                print(f"  ERRO: Arquivo não gerado")
                
        except Exception as e:
            print(f"  ERRO: {e}")
    else:
        print(f"  ERRO: Pasta nao encontrada")
        print(f"  Procurou por: {nome_cidade}")

print("\n" + "=" * 60)
print("Teste concluido!")
