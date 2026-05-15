import os
from pathlib import Path

# Lista de cidades no dicionário do app.py (extraído)
coordenadas_existe = {
    'balneario camboriu', 'balneário camboriú', 'camboriú', 'picarras', 'penha', 
    'porto belo', 'ilhota', 'itajaí', 'itapema', 'navegantes', 'tijucas', 
    'bom retiro do sul', 'bombinhas', 'barra velha', 'brusque', 'gaspar', 'blumenau', 
    'pomerode', 'botuverá', 'guabiruba', 'luiz alves', 'agronomica', 'dona emma', 
    'mirim doce', 'doutor pedrinho', 'witmarsum', 'canelinha', 'benedito novo', 
    'leoberto leal', 'indaial', 'timbó', 'ibirama', 'apiúna', 'rodeio', 
    'rio dos cedros', 'chapadão do lageado', 'ascurra', 'guide', 'vitor meireles', 
    'laurentino', 'nova trento', 'imbuia', 'lontras', 'vidal ramos', 'josé boiteux', 
    'rio do campo', 'agrolandia', 'atlanta', 'petrolândia', 'presidente nereu', 
    'braco do trombudo', 'trombudo central', 'rio do oeste', 'pouso redondo', 'salete', 
    'presidente getúlio', 'taió', 'aurora', 'ituparanga', 'santa terezinha', 
    'são joão batista'
}

# Cidades encontradas nas pastas
cidades_pastas = [
    'agrolandia', 'agronomica', 'apiuna', 'ascurra', 'atalanta', 'aurora',
    'balneario camboriu', 'balneario picarras', 'barra velha', 'benedito novo',
    'blumenau', 'bombinhas', 'botuvera', 'braco do trombudo', 'brusque', 'camboriu',
    'canelinha', 'chapadao do lageado', 'dona emma', 'doutor pedrinho', 'gaspar',
    'guabiruba', 'ibirama', 'ilhota', 'imbuia', 'indaial', 'itajai', 'itapema',
    'ituporanga', 'jose boiteux', 'laurentino', 'leoberto leal', 'lontras',
    'luiz alves', 'major gercino', 'mirim doce', 'navegantes', 'nova trento',
    'penha', 'petrolandia', 'pomerode', 'porto belo', 'pouso redondo',
    'presidente getulio', 'presidente nereu', 'rio do campo', 'rio do oeste',
    'rio do sul', 'rio dos cedros', 'rodeio', 'salete', 'santa terezinha',
    'sao joao batista', 'taio', 'tijucas', 'timbo', 'trombudo central',
    'vale itajai', 'vidal ramos', 'vitor meireles', 'witmarsum'
]

# Encontrar cidades faltando
faltando = []
for cidade in cidades_pastas:
    found = False
    for existente in coordenadas_existe:
        if cidade.lower() == existente.lower() or existente.lower().startswith(cidade.lower()):
            found = True
            break
    if not found:
        faltando.append(cidade)

print("CIDADES FALTANDO NO DICIONÁRIO COORDENADAS_CIDADES:")
print("=" * 60)
for cidade in sorted(set(faltando)):
    print(f"  ✗ {cidade.title()}")
