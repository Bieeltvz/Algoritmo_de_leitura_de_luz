"""
Aplicação web Flask para análise de imagens TIFF de satélite
Interface bonita para escolher e analisar imagens
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import json
import numpy as np
import rasterio
from leitura_de_luz import AnalisadorLuzSatelite
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# ⭐ DIRETÓRIO DE TRABALHO - Onde os CSVs e caches são salvos
DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
os.chdir(DIRETORIO_TRABALHO)  # Garantir que o Python está usando este diretório
logger.info(f"📁 Diretório de trabalho: {DIRETORIO_TRABALHO}")

# Diretório raiz de dados (onde estão todas as cidades)
CAMINHO_DOCUMENTOS = Path(r"C:\Users\gtvargas\Documents")

# Pasta selecionada atualmente (será inicializada automaticamente)
PASTA_SELECIONADA = {
    'caminho': None,
    'nome': None,
    'cidade': None,
    'tipo_recorte': None,
    'nome_amigavel': None,
    'total_imagens': 0
}

# Coordenadas das cidades do Vale do Itajaí e região (latitude, longitude)
# Coordenadas precisas obtidas do Nominatim/OpenStreetMap - IBGE centroide
COORDENADAS_CIDADES = {
    # Cidades Costeiras
    'balneario camboriu': (-26.9924, -48.634),
    'balneário camboriú': (-26.9924, -48.634),
    'camboriú': (-26.9924, -48.634),
    'camboriu': (-26.9924, -48.634),  # Alias sem acento
    'balneario picarras': (-26.8830, -48.6850),  # Entre Itajaí e Picarras
    'picarras': (-26.7639, -48.6717),  # Diferente de Balneário
    'penha': (-26.7754, -48.6465),
    'porto belo': (-27.1542, -48.5424),
    'ilhota': (-26.9023, -48.8285),
    'itajaí': (-26.9047, -48.6553),
    'itajai': (-26.9047, -48.6553),  # Alias sem acento
    'itapema': (-27.0947, -48.6138),
    'navegantes': (-26.8899, -48.6496),
    'tijucas': (-27.2394, -48.6354),
    'bom retiro do sul': (-29.6000, -51.9359),  # Localizado em Rio Grande do Sul (não em SC)
    'bombinhas': (-27.1519, -48.4876),
    'barra velha': (-26.6338, -48.6835),
    
    # Região Central
    'brusque': (-27.0965, -48.9136),
    'gaspar': (-26.9307, -48.9567),
    'blumenau': (-26.9196, -49.0658),
    'pomerode': (-26.7356, -49.177),
    'botuverá': (-27.1991, -49.0726),
    'botuvera': (-27.1991, -49.0726),  # Alias sem acento
    'guabiruba': (-27.0864, -48.9781),
    'luiz alves': (-26.7119, -48.9127),
    'agronomica': (-27.2661, -49.7105),
    'dona emma': (-26.9849, -49.7265),
    'mirim doce': (-27.2004, -50.0697),
    'doutor pedrinho': (-26.7164, -49.4827),
    'witmarsum': (-26.9275, -49.7947),
    'canelinha': (-27.266, -48.7667),
    'benedito novo': (-26.7841, -49.363),
    'leoberto leal': (-27.5071, -49.2872),
    
    # Região Alto Vale
    'indaial': (-26.8902, -49.2417),
    'timbó': (-26.8283, -49.2706),
    'timbo': (-26.8283, -49.2706),  # Alias sem acento
    'ibirama': (-27.0537, -49.5191),
    'apiúna': (-27.0375, -49.3885),
    'apiuna': (-27.0375, -49.3885),  # Alias sem acento
    'rodeio': (-26.9233, -49.3685),
    'rio dos cedros': (-26.7398, -49.2718),
    'chapadão do lageado': (-27.5905, -49.5539),
    'chapadao do lageado': (-27.5905, -49.5539),  # Alias sem acento
    'ascurra': (-26.957, -49.3768),
    'guide': (-27.2300, -49.3200),  # Alto Vale - coordenadas precisas do IBGE
    'vitor meireles': (-27.2842, -49.3947),
    'laurentino': (-27.2193, -49.7323),
    'nova trento': (-27.2863, -48.9303),
    
    # Região Sudoeste/Sul
    'imbuia': (-27.4908, -49.4218),
    'lontras': (-27.168, -49.5425),
    'vidal ramos': (-27.3909, -49.3616),
    'josé boiteux': (-26.9621, -49.6263),
    'jose boiteux': (-26.9621, -49.6263),  # Alias sem acento
    'rio do campo': (-26.9468, -50.1413),
    'rio do sul': (-27.7807, -49.6333),  # Rio do Sul - Alto Vale/Sudoeste
    'agrolandia': (-27.4121, -49.8295),
    'atlanta': (-27.2500, -49.5300),  # Vale do Itajaí - Nominatim corrigido (retornou Forquilhinha)
    'atalanta': (-27.2500, -49.5300),  # Alias (grafia alternativa)
    'petrolândia': (-27.533, -49.6985),
    'petrolandia': (-27.533, -49.6985),  # Alias sem acento
    'presidente nereu': (-27.2783, -49.389),
    'braco do trombudo': (-27.3586, -49.8821),
    'trombudo central': (-27.3041, -49.7932),
    'rio do oeste': (-27.1933, -49.7985),
    'pouso redondo': (-27.2567, -49.9332),
    'salete': (-26.9842, -50.0076),
    'presidente getúlio': (-27.0426, -49.621),
    'presidente getulio': (-27.0426, -49.621),  # Alias sem acento
    'taió': (-27.1168, -50.0002),
    'taio': (-27.1168, -50.0002),  # Alias sem acento
    'aurora': (-27.3304, -49.5866),
    'ituparanga': (-27.2900, -49.7100),  # Alto Vale - coordenadas precisas do IBGE
    'ituporanga': (-27.2900, -49.7100),  # Alias (grafia alternativa)
    'santa terezinha': (-26.7813, -50.009),
    'são joão batista': (-27.2775, -48.8496),
    'sao joao batista': (-27.2775, -48.8496),  # Alias sem acento
    'major gercino': (-27.0500, -49.4800),  # Major Gercino - Alto Vale
    'vale itajai': (-27.0790, -49.0630),  # Vale do Itajaí (região geral - centro do mapa)
}

# Centro do mapa (Vale do Itajaí - Blumenau como referência)
CENTRO_MAPA = (-27.0790, -49.0630)
ZOOM_INICIAL = 11

def descobrir_pastas_cidades():
    """
    Descobre automaticamente todas as cidades e suas pastas de recorte
    Procura por padrão muito flexível:
    - Documents/*noturno* ou *noturna* → Raster/RASTER → Qualquer pasta com .tif
    """
    pastas_encontradas = {}
    
    if not CAMINHO_DOCUMENTOS.exists():
        logger.warning(f"Documentos não encontrado: {CAMINHO_DOCUMENTOS}")
        return pastas_encontradas
    
    try:
        # Procura pastas com padrão "*noturno*" ou "*noturna*"
        for cidade_dir in CAMINHO_DOCUMENTOS.iterdir():
            if not cidade_dir.is_dir():
                continue
            
            nome_cidade = cidade_dir.name.lower()
            # Verifica se contém 'noturno' ou 'noturna'
            if not ('noturno' in nome_cidade or 'noturna' in nome_cidade):
                continue
            
            # Dentro procura por "Raster" ou "RASTER" (case-insensitive)
            raster_dir = None
            for item in cidade_dir.iterdir():
                if item.is_dir() and item.name.lower() == 'raster':
                    raster_dir = item
                    break
            
            if not raster_dir:
                continue
            
            # Dentro de Raster procura por QUALQUER pasta que contenha .tif
            for recorte_dir in raster_dir.iterdir():
                if not recorte_dir.is_dir():
                    continue
                
                # Contar imagens nesta pasta (procura recursivamente)
                total_imagens = len(list(recorte_dir.glob('*/*.tif'))) + len(list(recorte_dir.glob('*.tif')))
                
                # Se não tem imagens, pula
                if total_imagens == 0:
                    continue
                
                # Extrair nome amigável
                # Remove "_noturno", "_noturna" e formata
                cidade_nome = cidade_dir.name.replace('_noturno', '').replace('_noturna', '').replace('_', ' ').strip()
                
                # ⭐ LÓGICA MELHORADA PARA DIFERENCIAÇÃO
                # Usar o nome original do diretório de recorte para evitar conflitos
                # Exemplo: picarras_recortado vs Picarras_recorte devem ser diferenciados
                recorte_nome_original = recorte_dir.name.lower()
                
                # Se o nome contém "reprojetado" ou "reprojet", usar esse tipo
                if 'reprojet' in recorte_nome_original:
                    recorte_tipo = 'Reprojetados'
                else:
                    # Remover sufixos e manter o nome específico
                    recorte_tipo = recorte_dir.name.replace('_recorte', '').replace('_recortes', '').replace('_recortado', '').replace('_', ' ').strip()
                    
                    # Se ficou vazio ou é igual à cidade, usar nome original formatado
                    if not recorte_tipo or recorte_tipo.lower() == cidade_nome.lower():
                        recorte_tipo = recorte_dir.name.replace('_', ' ').strip()
                    
                    # Se ainda assim estiver vazio, usar "Recorte"
                    if not recorte_tipo:
                        recorte_tipo = 'Recorte'
                
                # Formatar com title case
                cidade_nome = cidade_nome.title()
                recorte_tipo = recorte_tipo.title()
                
                chave = f"{recorte_dir.name}"
                nome_amigavel = f"{cidade_nome} - {recorte_tipo}".strip()
                
                pastas_encontradas[chave] = {
                    'caminho': recorte_dir,
                    'nome': recorte_dir.name,
                    'cidade': cidade_nome,
                    'tipo_recorte': recorte_tipo,
                    'nome_amigavel': nome_amigavel,
                    'total_imagens': total_imagens,
                    'cidade_dir': cidade_dir
                }
                
                logger.info(f"Cidade encontrada: {nome_amigavel} ({total_imagens} imagens)")
    except Exception as e:
        logger.error(f"Erro ao descobrir pastas: {e}")
    
    return pastas_encontradas

# Descobrir pastas no startup
PASTAS_DISPONIVEIS = descobrir_pastas_cidades()

# Inicializar com primeira pasta encontrada
if PASTAS_DISPONIVEIS:
    primeira_pasta = list(PASTAS_DISPONIVEIS.values())[0]
    PASTA_SELECIONADA['caminho'] = primeira_pasta['caminho']
    PASTA_SELECIONADA['nome'] = primeira_pasta['nome']
    PASTA_SELECIONADA['cidade'] = primeira_pasta['cidade']
    PASTA_SELECIONADA['tipo_recorte'] = primeira_pasta['tipo_recorte']
    PASTA_SELECIONADA['nome_amigavel'] = primeira_pasta['nome_amigavel']
    PASTA_SELECIONADA['total_imagens'] = primeira_pasta['total_imagens']
    logger.info(f"Pasta inicial: {primeira_pasta['nome_amigavel']}")
else:
    logger.warning("Nenhuma pasta de cidades encontrada em Documentos")

def listar_imagens():
    """Lista todas as imagens TIFF disponíveis da pasta selecionada"""
    imagens = []
    caminho_pasta = PASTA_SELECIONADA['caminho']
    
    if not caminho_pasta.exists():
        return imagens
    
    for ano_dir in sorted(caminho_pasta.glob("*/"), reverse=True):
        if ano_dir.is_dir():
            ano = ano_dir.name
            imagens_ano = []
            for tif_file in sorted(ano_dir.glob("*.tif")):
                if not tif_file.name.endswith('.aux.xml'):
                    imagens_ano.append({
                        'nome': tif_file.name,
                        'caminho': str(tif_file),
                        'tamanho_kb': tif_file.stat().st_size / 1024,
                    })
            if imagens_ano:
                imagens.append({
                    'ano': ano,
                    'imagens': imagens_ano,
                    'total': len(imagens_ano)
                })
    return imagens

def analisar_tiff(caminho_arquivo):
    """Analisa uma imagem TIFF e retorna estatísticas"""
    try:
        caminho = Path(caminho_arquivo)
        
        if not caminho.exists():
            return {'erro': 'Arquivo não encontrado'}
        
        # Carregar com rasterio
        with rasterio.open(caminho) as src:
            imagem = src.read()
            if len(imagem.shape) > 2:
                imagem = imagem[0]
            imagem = np.array(imagem, dtype=float)
        
        # ⭐ NÃO USAR NORMALIZAÇÃO MIN-MAX!
        # Motivo: Cada imagem tem escala diferente, impossível comparar ao longo do tempo
        # Os dados de satélite já vêm calibrados em radiância/iluminância
        # Usar os valores originais para análise consistente
        
        # Ajustar tamanho esperado do analisador dinamicamente
        analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0, modo_geoespacial=True)
        tamanho_original = analisador.TAMANHO_ESPERADO
        analisador.TAMANHO_ESPERADO = imagem.shape
        
        # Processar
        stats = analisador.processar_imagem(imagem)
        
        # Restaurar tamanho
        analisador.TAMANHO_ESPERADO = tamanho_original
        
        # Determinar status de qualidade baseado no percentual válido (já excluindo NoData)
        if stats.percentual_valido >= 90:
            status = "✓ ACEITA"
            status_class = "success"
        elif stats.percentual_valido >= 70:
            status = "⚠ VERIFICAR"
            status_class = "warning"
        else:
            status = "✗ REJEITADA"
            status_class = "danger"
        
        # Calcular totais com dados (excluindo NoData)
        total_com_dados = stats.total_pixels - stats.pixels_nodata
        percentual_nulos = (100 * stats.pixels_nulos / total_com_dados) if total_com_dados > 0 else 0
        percentual_outliers = (100 * stats.pixels_outliers / total_com_dados) if total_com_dados > 0 else 0
        
        return {
            'sucesso': True,
            'nome_arquivo': caminho.name,
            'dimensoes': f"{imagem.shape[0]} × {imagem.shape[1]}",
            'total_pixels': f"{stats.total_pixels:,}",
            'pixels_validos': f"{stats.pixels_validos:,}",
            'percentual_valido': f"{stats.percentual_valido:.2f}%",
            'pixels_nulos': f"{stats.pixels_nulos:,}",
            'percentual_nulos': f"{percentual_nulos:.2f}%",
            'pixels_outliers': f"{stats.pixels_outliers:,}",
            'percentual_outliers': f"{percentual_outliers:.2f}%",
            'pixels_nodata': f"{stats.pixels_nodata:,}",
            'percentual_nodata': f"{100*stats.pixels_nodata/stats.total_pixels:.2f}%",
            'intensidade_media': f"{stats.intensidade_media:.2f}",
            'intensidade_mediana': f"{stats.intensidade_mediana:.2f}",
            'intensidade_minima': f"{stats.intensidade_minima:.2f}",
            'intensidade_maxima': f"{stats.intensidade_maxima:.2f}",
            'desvio_padrao': f"{stats.desvio_padrao:.2f}",
            'threshold_outlier': f"{stats.threshold_outlier:.2f}",
            'threshold_crescimento_luz': f"{stats.threshold_crescimento_luz:.2f}",
            'status': status,
            'status_class': status_class,
        }
    except Exception as e:
        logger.error(f"Erro ao analisar: {e}")
        return {'erro': f"Erro ao processar: {str(e)}"}

@app.route('/')
def index():
    """Página principal"""
    imagens = listar_imagens()
    return render_template('index.html', imagens=imagens)

@app.route('/api/listar-imagens')
def api_listar_imagens():
    """API para listar imagens"""
    imagens = listar_imagens()
    return jsonify(imagens)

@app.route('/api/analisar', methods=['POST'])
def api_analisar():
    """API para analisar uma imagem"""
    data = request.get_json()
    caminho = data.get('caminho')
    
    if not caminho:
        return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
    
    resultado = analisar_tiff(caminho)
    return jsonify(resultado)

@app.route('/api/analisar-upload', methods=['POST'])
def api_analisar_upload():
    """API para analisar arquivo enviado via upload"""
    if 'file' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo foi enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'erro': 'Arquivo vazio'}), 400
    
    if not file.filename.lower().endswith(('.tif', '.tiff')):
        return jsonify({'erro': 'Arquivo deve ser um TIFF (.tif ou .tiff)'}), 400
    
    try:
        import tempfile
        # Ler o arquivo na memória
        file_data = file.read()
        
        # Salvar arquivo temporário
        import io
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
                tmp.write(file_data)
                temp_path = tmp.name
            
            # Analisar
            resultado = analisar_tiff(temp_path)
            return jsonify(resultado)
        finally:
            # Limpar arquivo temporário
            if temp_path:
                try:
                    import time
                    time.sleep(0.1)  # Aguardar para liberar arquivo
                    os.unlink(temp_path)
                except:
                    pass  # Ignorar erros de deleção
    except Exception as e:
        logger.error(f"Erro ao analisar upload: {e}")
        return jsonify({'erro': f'Erro ao processar arquivo: {str(e)}'}), 500

@app.route('/resultado')
def resultado():
    """Página de resultados"""
    return render_template('resultado.html')

@app.route('/api/comparar-crescimento', methods=['POST'])
def api_comparar_crescimento():
    """API para comparar crescimento de luz entre dois arquivos"""
    try:
        data = request.get_json()
        arquivo_anterior = data.get('arquivo_anterior')
        arquivo_atual = data.get('arquivo_atual')
        
        if not arquivo_anterior or not arquivo_atual:
            return jsonify({'erro': 'Dois arquivos são necessários para comparação'}), 400
        
        # Analisar ambos os arquivos
        stats_anterior_data = analisar_tiff(arquivo_anterior)
        stats_atual_data = analisar_tiff(arquivo_atual)
        
        if 'erro' in stats_anterior_data or 'erro' in stats_atual_data:
            return jsonify({'erro': 'Erro ao analisar um ou ambos os arquivos'}), 400
        
        # Converter de string para float para comparação
        class StatsObj:
            pass
        
        stats_anterior = StatsObj()
        stats_anterior.intensidade_media = float(stats_anterior_data['intensidade_media'])
        stats_anterior.threshold_crescimento_luz = float(stats_anterior_data['threshold_crescimento_luz'])
        stats_anterior.desvio_padrao = float(stats_anterior_data['desvio_padrao'])
        stats_anterior.percentual_valido = float(stats_anterior_data['percentual_valido'].rstrip('%'))
        
        stats_atual = StatsObj()
        stats_atual.intensidade_media = float(stats_atual_data['intensidade_media'])
        stats_atual.threshold_crescimento_luz = float(stats_atual_data['threshold_crescimento_luz'])
        stats_atual.desvio_padrao = float(stats_atual_data['desvio_padrao'])
        stats_atual.percentual_valido = float(stats_atual_data['percentual_valido'].rstrip('%'))
        
        # Usar o analisador para comparar
        analisador = AnalisadorLuzSatelite()
        comparacao = analisador.comparar_crescimento_luz(stats_anterior, stats_atual)
        
        # Formatar resultado
        return jsonify({
            'sucesso': True,
            'arquivo_anterior': Path(arquivo_anterior).name,
            'arquivo_atual': Path(arquivo_atual).name,
            'intensidade_media_anterior': stats_anterior_data['intensidade_media'],
            'intensidade_media_atual': stats_atual_data['intensidade_media'],
            'threshold_anterior': stats_anterior_data['threshold_crescimento_luz'],
            'threshold_atual': stats_atual_data['threshold_crescimento_luz'],
            'crescimento_media': f"{comparacao['crescimento_media']:+.2f}",
            'percentual_crescimento': f"{comparacao['percentual_crescimento']:+.2f}%",
            'status_crescimento': comparacao['status_crescimento'],
            'crescimento_significativo': comparacao['crescimento_significativo'],
            'diferenca_thresholds': f"{comparacao['diferenca_thresholds']:+.2f}",
        })
    except Exception as e:
        logger.error(f"Erro ao comparar crescimento: {e}")
        return jsonify({'erro': f'Erro ao comparar: {str(e)}'}), 500

@app.route('/api/processar-paralelo', methods=['POST'])
def api_processar_paralelo():
    """Inicia processamento paralelo de todas as imagens da pasta selecionada"""
    try:
        from processador_paralelo import ProcessadorParalelo
        import threading
        
        # Usar nome da cidade como prefixo dos arquivos
        nome_cidade = PASTA_SELECIONADA['nome']
        
        # Verificar se deve forçar reprocessamento
        dados = request.get_json() or {}
        forcar = dados.get('forcar_reprocessamento', False)
        
        def processar_background():
            logger.info(f"Iniciando processamento paralelo em {PASTA_SELECIONADA['nome_amigavel']}...")
            # Passar nome_cidade, forcar_reprocessamento e diretorio_trabalho
            processador = ProcessadorParalelo(
                nome_cidade=nome_cidade, 
                forcar_reprocessamento=forcar,
                diretorio_trabalho=str(DIRETORIO_TRABALHO)
            )
            processador.processar_pasta(str(PASTA_SELECIONADA['caminho']))
            logger.info(f"Processamento paralelo de {nome_cidade} concluído!")
        
        # Executar em thread separada para não bloquear a interface
        thread = threading.Thread(target=processar_background, daemon=True)
        thread.start()
        
        return jsonify({
            'sucesso': True,
            'mensagem': f'Processamento iniciado para {PASTA_SELECIONADA["nome_amigavel"]}. Você será notificado quando terminar.',
            'cidade': PASTA_SELECIONADA['nome_amigavel'],
            'forcar_reprocessamento': forcar
        })
    except Exception as e:
        logger.error(f"Erro ao iniciar processamento paralelo: {e}")
        return jsonify({'erro': f'Erro ao iniciar processamento: {str(e)}'}), 500

@app.route('/api/resultados', methods=['GET'])
def api_resultados():
    """Retorna os resultados do CSV de processamento paralelo da pasta selecionada"""
    try:
        import csv
        from pathlib import Path
        
        # Usar nome da cidade para localizar arquivo específico
        nome_cidade = PASTA_SELECIONADA['nome']
        arquivo_csv = DIRETORIO_TRABALHO / f'resultados_{nome_cidade}.csv'
        
        logger.info(f"🔍 Procurando arquivo CSV: {arquivo_csv}")
        
        if not arquivo_csv.exists():
            logger.warning(f"❌ Arquivo não encontrado: {arquivo_csv}")
            return jsonify({
                'sucesso': False,
                'mensagem': f'Nenhum resultado disponível ainda. Execute o processamento paralelo primeiro.',
                'debug': f'Arquivo esperado: {arquivo_csv}'
            })
        
        # Ler CSV
        resultados = []
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                # CSV vazio (nem cabeçalho tem)
                logger.warning(f"⚠️  CSV vazio (sem cabeçalho): {arquivo_csv}")
                return jsonify({
                    'sucesso': False,
                    'mensagem': f'Processamento não foi executado ainda. Clique em "Iniciar Processamento Paralelo".'
                })
            
            for row in reader:
                resultados.append(row)
        
        logger.info(f"✅ Lidos {len(resultados)} resultados do CSV")
        
        # Se o CSV tem cabeçalho mas sem dados
        if not resultados:
            logger.warning(f"⚠️  CSV com cabeçalho mas sem dados: {arquivo_csv}")
            return jsonify({
                'sucesso': False,
                'mensagem': f'Nenhum resultado disponível. O processamento pode ter encontrado um erro. Tente executar novamente.'
            })
        
        # Calcular estatísticas
        medias = [float(r['intensidade_media']) for r in resultados]
        anos_unicos = set(r['ano'] for r in resultados)
        
        return jsonify({
            'sucesso': True,
            'total_registros': len(resultados),
            'media_geral': f"{sum(medias)/len(medias):.2f}",
            'minimo': f"{min(medias):.2f}",
            'maximo': f"{max(medias):.2f}",
            'anos': sorted(list(anos_unicos)),
            'resultados': resultados  # Todos os registros
        })
    except Exception as e:
        logger.error(f"Erro ao ler resultados: {e}")
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao ler resultados: {str(e)}'
        }), 500

@app.route('/api/tendencias', methods=['GET'])
def api_tendencias():
    """Retorna análise de tendências da pasta selecionada"""
    try:
        from tendencias import AnalisadorTendencias
        from pathlib import Path
        
        # Usar arquivo específico por cidade
        nome_cidade = PASTA_SELECIONADA['nome']
        arquivo_csv = DIRETORIO_TRABALHO / f'resultados_{nome_cidade}.csv'
        
        if not arquivo_csv.exists():
            return jsonify({
                'sucesso': False,
                'mensagem': f'Nenhum resultado disponível para {PASTA_SELECIONADA["nome_amigavel"]}'
            })
        
        analisador = AnalisadorTendencias()
        if not analisador.ler_csv(str(arquivo_csv)):
            return jsonify({
                'sucesso': False,
                'mensagem': 'Erro ao ler arquivo de resultados'
            })
        
        tendencias = analisador.calcular_tendencias()
        
        # Formatar para retornar
        dados_tendencias = []
        for ano in sorted(tendencias.keys()):
            stats = tendencias[ano]
            dados_tendencias.append({
                'ano': ano,
                'media': f"{stats['media']:.2f}",
                'minimo': f"{stats['minimo']:.2f}",
                'maximo': f"{stats['maximo']:.2f}",
                'desvio': f"{stats['desvio']:.2f}",
                'registros': stats['registros']
            })
        
        return jsonify({
            'sucesso': True,
            'tendencias': dados_tendencias
        })
    except Exception as e:
        logger.error(f"Erro ao calcular tendências: {e}")
        return jsonify({'erro': f'Erro ao calcular tendências: {str(e)}'}), 500

@app.route('/api/status-processamento', methods=['GET'])
def api_status_processamento():
    """Retorna status do processamento paralelo da pasta selecionada"""
    try:
        from pathlib import Path
        import json
        
        # Usar arquivos específicos por cidade
        nome_cidade = PASTA_SELECIONADA['nome']
        cache_file = DIRETORIO_TRABALHO / f'processados_{nome_cidade}.json'
        resultados_file = DIRETORIO_TRABALHO / f'resultados_{nome_cidade}.csv'
        
        logger.debug(f"🔍 Procurando status - Cache: {cache_file}, Resultados: {resultados_file}")
        
        processados_count = 0
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cache = json.load(f)
                processados_count = len(cache)
        
        resultados_count = 0
        if resultados_file.exists():
            import csv
            with open(resultados_file, 'r', encoding='utf-8') as f:
                # Contar linhas de dados (excluindo cabeçalho)
                reader = csv.DictReader(f)
                resultados_count = sum(1 for _ in reader)
        
        logger.debug(f"📊 Status - Processados: {processados_count}, Resultados: {resultados_count}")
        
        return jsonify({
            'sucesso': True,
            'processados': processados_count,
            'resultados': resultados_count,
            'cache_existe': cache_file.exists(),
            'resultados_existe': resultados_file.exists()
        })
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        return jsonify({'erro': str(e)}), 500

@app.route('/api/listar-pastas', methods=['GET'])
def api_listar_pastas():
    """Lista todas as pastas de imagens disponíveis (cidades descobertas)"""
    try:
        pastas = []
        
        for chave, info in sorted(PASTAS_DISPONIVEIS.items()):
            pastas.append({
                'nome': info['nome'],
                'nome_amigavel': info['nome_amigavel'],
                'cidade': info['cidade'],
                'tipo_recorte': info['tipo_recorte'],
                'caminho': str(info['caminho']),
                'total_imagens': info['total_imagens'],
                'selecionada': PASTA_SELECIONADA['nome'] == info['nome']
            })
        
        return jsonify({
            'sucesso': True,
            'pastas': pastas,
            'pasta_atual': PASTA_SELECIONADA['nome'],
            'total_cidades': len(pastas)
        })
    except Exception as e:
        logger.error(f"Erro ao listar pastas: {e}")
        return jsonify({'erro': str(e)}), 500

@app.route('/api/coordenadas-cidades', methods=['GET'])
def api_coordenadas_cidades():
    """Retorna coordenadas de todas as cidades para o mapa interativo"""
    try:
        cidades_com_coords = {}
        
        for chave, info in PASTAS_DISPONIVEIS.items():
            # Procura pela coordenada usando o nome da cidade
            cidade_lower = info['cidade'].lower()
            
            # Tenta correspondência exata
            if cidade_lower in COORDENADAS_CIDADES:
                coord = COORDENADAS_CIDADES[cidade_lower]
            else:
                # Tenta correspondência parcial
                coord = None
                for cidade_chave, coord_valor in COORDENADAS_CIDADES.items():
                    if cidade_chave in cidade_lower or cidade_lower in cidade_chave:
                        coord = coord_valor
                        break
            
            if coord:
                cidades_com_coords[chave] = {
                    'nome_amigavel': info['nome_amigavel'],
                    'lat': coord[0],
                    'lng': coord[1],
                    'total_imagens': info['total_imagens']
                }
        
        return jsonify({
            'sucesso': True,
            'cidades': cidades_com_coords,
            'centro': {'lat': CENTRO_MAPA[0], 'lng': CENTRO_MAPA[1]},
            'zoom': ZOOM_INICIAL
        })
    except Exception as e:
        logger.error(f"Erro ao obter coordenadas: {e}")
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

@app.route('/api/selecionar-pasta', methods=['POST'])
def api_selecionar_pasta():
    """Seleciona a pasta de imagens a utilizar"""
    try:
        dados = request.json
        nome_pasta = dados.get('nome_pasta')
        
        if not nome_pasta:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Nome da pasta não fornecido'
            })
        
        if nome_pasta not in PASTAS_DISPONIVEIS:
            return jsonify({
                'sucesso': False,
                'mensagem': f'Pasta não encontrada: {nome_pasta}'
            })
        
        info_pasta = PASTAS_DISPONIVEIS[nome_pasta]
        
        # Atualizar pasta selecionada globalmente
        PASTA_SELECIONADA['caminho'] = info_pasta['caminho']
        PASTA_SELECIONADA['nome'] = info_pasta['nome']
        PASTA_SELECIONADA['cidade'] = info_pasta['cidade']
        PASTA_SELECIONADA['tipo_recorte'] = info_pasta['tipo_recorte']
        PASTA_SELECIONADA['nome_amigavel'] = info_pasta['nome_amigavel']
        PASTA_SELECIONADA['total_imagens'] = info_pasta['total_imagens']
        
        logger.info(f"Pasta selecionada: {info_pasta['nome_amigavel']}")
        
        return jsonify({
            'sucesso': True,
            'mensagem': f"Pasta selecionada: {info_pasta['nome_amigavel']}",
            'pasta_atual': nome_pasta,
            'nome_amigavel': info_pasta['nome_amigavel'],
            'cidade': info_pasta['cidade'],
            'total_imagens': info_pasta['total_imagens']
        })
    except Exception as e:
        logger.error(f"Erro ao selecionar pasta: {e}")
        return jsonify({'erro': str(e)}), 500

@app.route('/api/pasta-atual', methods=['GET'])
def api_pasta_atual():
    """Retorna a pasta atualmente selecionada"""
    return jsonify({
        'sucesso': True,
        'nome': PASTA_SELECIONADA['nome'],
        'nome_amigavel': PASTAS_DISPONIVEIS.get(PASTA_SELECIONADA['nome'], {}).get('nome_amigavel', PASTA_SELECIONADA['nome']),
        'cidade': PASTA_SELECIONADA['cidade'],
        'tipo_recorte': PASTA_SELECIONADA['tipo_recorte'],
        'caminho': str(PASTA_SELECIONADA['caminho']) if PASTA_SELECIONADA['caminho'] else None
    })

@app.route('/api/sugerir-thresholds', methods=['GET'])
def api_sugerir_thresholds():
    """Analisa dados anuais e sugere valores de threshold para crescimento de luz"""
    try:
        from sugestores_threshold import analisar_e_sugerir_thresholds
        from pathlib import Path
        
        # Usar arquivo específico por cidade
        nome_cidade = PASTA_SELECIONADA['nome']
        arquivo_csv = DIRETORIO_TRABALHO / f'resultados_{nome_cidade}.csv'
        
        logger.info(f"🔍 Sugerindo thresholds para {PASTA_SELECIONADA['nome_amigavel']}")
        
        if not arquivo_csv.exists():
            logger.warning(f"❌ Arquivo não encontrado: {arquivo_csv}")
            return jsonify({
                'sucesso': False,
                'mensagem': f'Nenhum resultado disponível para {PASTA_SELECIONADA["nome_amigavel"]}. Execute o processamento paralelo primeiro.',
                'debug': f'Arquivo esperado: {arquivo_csv}'
            })
        
        # Analisar e gerar sugestões
        sugestoes = analisar_e_sugerir_thresholds(str(arquivo_csv))
        
        if 'erro' in sugestoes:
            logger.error(f"Erro ao analisar: {sugestoes['erro']}")
            return jsonify({
                'sucesso': False,
                'mensagem': sugestoes['erro']
            })
        
        logger.info(f"✅ Sugestões geradas com sucesso para {nome_cidade}")
        
        return jsonify({
            'sucesso': True,
            'cidade': PASTA_SELECIONADA['nome_amigavel'],
            'dados': sugestoes
        })
    
    except Exception as e:
        logger.error(f"Erro ao sugerir thresholds: {e}")
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao sugerir thresholds: {str(e)}'
        }), 500

@app.route('/api/gerar-heatmap', methods=['GET'])
def api_gerar_heatmap():
    """Gera heatmap de crescimento luminoso para a cidade selecionada"""
    try:
        from heatmap_crescimento import HeatmapCrescimento
        
        nome_cidade = PASTA_SELECIONADA['nome']
        arquivo_csv = DIRETORIO_TRABALHO / f'resultados_{nome_cidade}.csv'
        
        logger.info(f"🗺️ Gerando heatmap para {PASTA_SELECIONADA['nome_amigavel']}")
        
        if not arquivo_csv.exists():
            return jsonify({
                'sucesso': False,
                'mensagem': f'Nenhum resultado disponível para {PASTA_SELECIONADA["nome_amigavel"]}. Execute o processamento primeiro.',
            })
        
        # Criar gerador
        gerador = HeatmapCrescimento()
        
        # Ler dados
        if not gerador.ler_csv(str(arquivo_csv)):
            return jsonify({
                'sucesso': False,
                'mensagem': 'Erro ao ler dados do CSV'
            })
        
        # Gerar heatmaps
        arquivo_crescimento = DIRETORIO_TRABALHO / f'heatmap_crescimento_{nome_cidade}.png'
        arquivo_intensidade = DIRETORIO_TRABALHO / f'heatmap_intensidade_{nome_cidade}.png'
        arquivo_comparativo = DIRETORIO_TRABALHO / f'heatmap_comparativo_{nome_cidade}.png'
        
        gerador.gerar_heatmap_crescimento(str(arquivo_crescimento))
        gerador.gerar_heatmap_intensidade(str(arquivo_intensidade))
        gerador.gerar_heatmap_comparativo(str(arquivo_comparativo))
        
        # Gerar relatório
        relatorio = gerador.gerar_relatorio()
        
        logger.info(f"✅ Heatmaps gerados com sucesso para {nome_cidade}")
        
        return jsonify({
            'sucesso': True,
            'cidade': PASTA_SELECIONADA['nome_amigavel'],
            'mensagem': 'Heatmaps gerados com sucesso!',
            'arquivos': {
                'crescimento': f'heatmap_crescimento_{nome_cidade}.png',
                'intensidade': f'heatmap_intensidade_{nome_cidade}.png',
                'comparativo': f'heatmap_comparativo_{nome_cidade}.png'
            },
            'relatorio': relatorio
        })
    
    except Exception as e:
        logger.error(f"Erro ao gerar heatmap: {e}")
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao gerar heatmap: {str(e)}'
        }), 500

@app.route('/heatmap/<filename>')
def servir_heatmap(filename):
    """Serve as imagens de heatmap"""
    try:
        return send_from_directory(DIRETORIO_TRABALHO, filename)
    except Exception as e:
        logger.error(f"Erro ao servir heatmap: {e}")
        return jsonify({'erro': 'Arquivo não encontrado'}), 404

@app.route('/api/gerar-mapa-crescimento', methods=['GET'])
def api_gerar_mapa_crescimento():
    """Gera mapa visual de crescimento luminoso para a cidade selecionada"""
    try:
        from mapa_crescimento import MapaCrescimento
        
        nome_cidade = PASTA_SELECIONADA['nome']
        nome_amigavel = PASTA_SELECIONADA['nome_amigavel']
        
        logger.info(f"🗺️ Gerando mapa de crescimento para {nome_amigavel}...")
        
        mapa = MapaCrescimento()
        
        # Carregar coordenadas
        if not mapa.carregar_coordenadas():
            return jsonify({
                'sucesso': False,
                'mensagem': 'Erro ao carregar coordenadas das cidades'
            })
        
        # Gerar HTML para a cidade específica
        arquivo_html = DIRETORIO_TRABALHO / f'mapa_{nome_cidade}.html'
        arquivo_gerado = mapa.gerar_relatorio_html_cidade(nome_cidade, str(arquivo_html))
        
        if not arquivo_gerado:
            return jsonify({
                'sucesso': False,
                'mensagem': f'Nenhum resultado disponível para {nome_amigavel}'
            })
        
        # Calcular dados para exibição
        dados_cidade = mapa.calcular_crescimento_cidade_unica(nome_cidade)
        
        logger.info(f"✅ Mapa gerado para {nome_amigavel}")
        
        return jsonify({
            'sucesso': True,
            'mensagem': f'Mapa gerado com sucesso para {nome_amigavel}!',
            'cidade': nome_amigavel,
            'crescimento': dados_cidade.get('crescimento', 0),
            'url_mapa': f'/mapa-crescimento-cidade?cidade={nome_cidade}'
        })
    
    except Exception as e:
        logger.error(f"Erro ao gerar mapa: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao gerar mapa: {str(e)}'
        }), 500

@app.route('/api/gerar-timelapse', methods=['GET'])
def api_gerar_timelapse():
    """Gera timelapse das imagens da cidade com overlay de crescimento"""
    try:
        from mapa_crescimento import MapaCrescimento
        
        nome_cidade = PASTA_SELECIONADA['nome']
        nome_amigavel = PASTA_SELECIONADA['nome_amigavel']
        caminho_pasta = str(PASTA_SELECIONADA['caminho'])
        
        logger.info(f"⏱️ Gerando timelapse para {nome_amigavel}...")
        
        mapa = MapaCrescimento()
        
        # Carregar coordenadas
        if not mapa.carregar_coordenadas():
            return jsonify({
                'sucesso': False,
                'mensagem': 'Erro ao carregar coordenadas das cidades'
            })
        
        # Gerar timelapse
        arquivo_html = DIRETORIO_TRABALHO / f'timelapse_{nome_cidade}.html'
        arquivo_gerado = mapa.gerar_timelapse_cidade(nome_cidade, caminho_pasta, str(arquivo_html))
        
        if not arquivo_gerado:
            return jsonify({
                'sucesso': False,
                'mensagem': f'Não foi possível gerar timelapse para {nome_amigavel}'
            })
        
        logger.info(f"✅ Timelapse gerado para {nome_amigavel}")
        
        return jsonify({
            'sucesso': True,
            'mensagem': f'Timelapse gerado com sucesso para {nome_amigavel}!',
            'cidade': nome_amigavel,
            'url_timelapse': f'/timelapse-cidade?cidade={nome_cidade}'
        })
    
    except Exception as e:
        logger.error(f"Erro ao gerar timelapse: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao gerar timelapse: {str(e)}'
        }), 500

@app.route('/mapa-crescimento-cidade')
def servir_mapa_crescimento_cidade():
    """Serve o mapa HTML para uma cidade específica"""
    try:
        cidade = request.args.get('cidade', PASTA_SELECIONADA['nome'])
        arquivo = DIRETORIO_TRABALHO / f'mapa_{cidade}.html'
        
        if arquivo.exists():
            return send_from_directory(DIRETORIO_TRABALHO, f'mapa_{cidade}.html')
        else:
            return '''
            <html>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1>Mapa não gerado</h1>
                    <p>Clique no botão "Gerar Mapa de Crescimento" para gerar o mapa interativo.</p>
                </body>
            </html>
            '''
    except Exception as e:
        logger.error(f"Erro ao servir mapa: {e}")
        return f"Erro: {str(e)}", 500

@app.route('/timelapse-cidade')
def servir_timelapse_cidade():
    """Serve o timelapse HTML para uma cidade específica"""
    try:
        cidade = request.args.get('cidade', PASTA_SELECIONADA['nome'])
        arquivo = DIRETORIO_TRABALHO / f'timelapse_{cidade}.html'
        
        if arquivo.exists():
            return send_from_directory(DIRETORIO_TRABALHO, f'timelapse_{cidade}.html')
        else:
            return '''
            <html>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1>Timelapse não gerado</h1>
                    <p>Clique no botão "Gerar Timelapse" para gerar o timelapse das imagens.</p>
                </body>
            </html>
            '''
    except Exception as e:
        logger.error(f"Erro ao servir timelapse: {e}")
        return f"Erro: {str(e)}", 500

@app.route('/mapa-crescimento')
def servir_mapa_crescimento():
    """Serve o mapa HTML interativo"""
    try:
        arquivo = DIRETORIO_TRABALHO / 'mapa_crescimento.html'
        if arquivo.exists():
            return send_from_directory(DIRETORIO_TRABALHO, 'mapa_crescimento.html')
        else:
            return '''
            <html>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1>Mapa não gerado</h1>
                    <p>Clique no botão "Gerar Mapa de Crescimento" para gerar o mapa interativo.</p>
                </body>
            </html>
            '''
    except Exception as e:
        logger.error(f"Erro ao servir mapa: {e}")
        return f"Erro: {str(e)}", 500

if __name__ == '__main__':
    # Criar diretório templates se não existir
    Path('templates').mkdir(exist_ok=True)
    Path('static').mkdir(exist_ok=True)
    
    print("\n" + "="*70)
    print("🌐 APLICAÇÃO DE ANÁLISE DE IMAGENS TIFF")
    print("="*70)
    print("\n📱 Acesse a aplicação em: http://localhost:5000")
    print("   (Aperte Ctrl+C para parar)\n")
    
    app.run(debug=True, port=5000)
