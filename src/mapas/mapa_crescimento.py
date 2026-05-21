import numpy as np
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Mapa Visual de Crescimento Luminoso
Cria um mapa interativo mostrando crescimento por cidade
"""

import json
from pathlib import Path
from collections import defaultdict
import csv
import logging
import os
import base64
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir diretório de trabalho - aponta para data/saida onde estão os CSVs
# Estrutura: src/mapas/mapa_crescimento.py -> ../../data/saida/
DIRETORIO_TRABALHO = (Path(__file__).parent.parent.parent / 'data' / 'saida').absolute()

# Se não existir, usar o diretório atual como fallback
if not DIRETORIO_TRABALHO.exists():
    logger.warning(f"⚠️  Diretório padrão não encontrado: {DIRETORIO_TRABALHO}")
    DIRETORIO_TRABALHO = Path.cwd()
    logger.info(f"📂 Usando diretório atual: {DIRETORIO_TRABALHO}")

os.chdir(DIRETORIO_TRABALHO)
logger.info(f"📂 Diretório de trabalho configurado: {DIRETORIO_TRABALHO}")


class MapaCrescimento:
    """Gera mapa visual de crescimento luminoso por cidade"""
    
    def __init__(self):
        """Inicializa o gerador"""
        self.crescimento_cidades = {}
        self.coordenadas = {}
    
    def encontrar_arquivo_csv(self, nome_cidade: str) -> str:
        """
        Encontra o arquivo CSV da cidade procurando por variações de nome.
        
        Tenta: resultados_NomeCidade.csv, resultados_NomeCidade_recorte.csv, etc.
        Usa mapeamento de cidades para encontrar nomes alternativos.
        
        Args:
            nome_cidade: Nome da cidade
            
        Returns:
            str: Caminho do arquivo CSV se encontrado, '' caso contrário
        """
        try:
            from difflib import SequenceMatcher
            
            # Padrões possíveis para o arquivo CSV
            padroes = [
                f'resultados_{nome_cidade}.csv',  # Sem sufixo
                f'resultados_{nome_cidade}_recorte.csv',  # Com _recorte
                f'resultados_{nome_cidade}_Recorte.csv',  # Com _Recorte
                f'resultados_{nome_cidade}_recortes.csv',  # Com _recortes
                f'resultados_{nome_cidade}_Recortes.csv',  # Com _Recortes
                f'resultados_{nome_cidade}_RECORTADO.csv',  # Com _RECORTADO
            ]
            
            # Locais a procurar
            locais = [
                DIRETORIO_TRABALHO,  # Diretório padrão configurado
                Path.cwd(),  # Diretório atual
                Path(__file__).parent.parent.parent / 'data' / 'saida',  # Estrutura nova
            ]
            
            # Tenta buscar primeiro com os padrões
            for local in locais:
                if not local.exists():
                    continue
                    
                for padrao in padroes:
                    arquivo = local / padrao
                    if arquivo.exists():
                        logger.info(f"✅ Arquivo encontrado: {arquivo}")
                        return str(arquivo)
            
            # Se não encontrar, tenta carregar mapeamento de cidades
            mapeamento_arquivo = Path(__file__).parent.parent.parent / 'data' / 'mapeamento_cidades.json'
            if mapeamento_arquivo.exists():
                try:
                    with open(mapeamento_arquivo, 'r', encoding='utf-8') as f:
                        import json
                        mapeamento_data = json.load(f)
                        mapeamento = mapeamento_data.get('mapeamento_cidades_arquivos', {})
                        
                        if nome_cidade in mapeamento:
                            nome_alternativo = mapeamento[nome_cidade]
                            padroes_alt = [
                                f'resultados_{nome_alternativo}.csv',
                                f'resultados_{nome_alternativo}_recorte.csv',
                                f'resultados_{nome_alternativo}_RECORTADO.csv',
                            ]
                            
                            for local in locais:
                                if not local.exists():
                                    continue
                                for padrao_alt in padroes_alt:
                                    arquivo = local / padrao_alt
                                    if arquivo.exists():
                                        logger.info(f"✅ Arquivo encontrado via mapeamento: {arquivo}")
                                        return str(arquivo)
                except Exception as e:
                    logger.debug(f"Erro ao carregar mapeamento: {e}")
            
            # Se não encontrar com padrões, procura por fuzzy matching
            logger.debug(f"Nenhum padrão exato encontrado para {nome_cidade}, procurando por fuzzy matching...")
            
            melhor_match = None
            melhor_score = 0.0
            
            for local in locais:
                if not local.exists():
                    continue
                    
                for arquivo in local.glob('resultados_*.csv'):
                    # Extrair o nome da cidade do nome do arquivo
                    nome_arquivo = arquivo.stem.replace('resultados_', '').lower()
                    
                    # Remover sufixos comuns
                    for sufixo in ['_recorte', '_recortes', '_recortado', '_reprojetado', '_noturno', '_noturna']:
                        nome_arquivo = nome_arquivo.replace(sufixo, '')
                    
                    # Calcular similaridade
                    ratio = SequenceMatcher(None, nome_cidade.lower(), nome_arquivo).ratio()
                    
                    if ratio > melhor_score:
                        melhor_score = ratio
                        melhor_match = arquivo
            
            # Se encontrou algo com score razoável (> 50%), retorna
            if melhor_match and melhor_score > 0.5:
                logger.info(f"✅ Arquivo encontrado por fuzzy matching (score: {melhor_score:.1%}): {melhor_match}")
                return str(melhor_match)
            
            logger.warning(f"❌ Nenhum arquivo de resultados encontrado para {nome_cidade}")
            logger.warning(f"Locais procurados: {[str(l) for l in locais if l.exists()]}")
            return ''
            
        except Exception as e:
            logger.error(f"Erro ao procurar arquivo CSV: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return ''
        
    def carregar_coordenadas(self, arquivo_json: str = 'coordenadas_cidades_completas_nominatim.json') -> bool:
        """
        Carrega coordenadas das cidades
        
        Args:
            arquivo_json: Arquivo com coordenadas (nome do arquivo ou caminho completo)
            
        Returns:
            bool: Sucesso na leitura
        """
        try:
            # Tentar diferentes caminhos
            caminhos_possiveis = [
                Path(arquivo_json),  # Caminho relativo direto
                Path(__file__).parent.parent.parent / 'data' / 'coordenadas' / arquivo_json,  # Estrutura nova
                Path.cwd() / arquivo_json,  # Diretório atual
                Path.cwd() / 'data' / 'coordenadas' / arquivo_json,  # De qualquer lugar
            ]
            
            caminho_encontrado = None
            for caminho in caminhos_possiveis:
                if caminho.exists():
                    caminho_encontrado = caminho
                    break
            
            if not caminho_encontrado:
                logger.warning(f"Arquivo não encontrado em nenhum caminho: {arquivo_json}")
                logger.warning(f"Caminhos testados: {[str(p) for p in caminhos_possiveis]}")
                return False
            
            logger.info(f"📂 Carregando coordenadas de: {caminho_encontrado}")
            with open(caminho_encontrado, 'r', encoding='utf-8') as f:
                self.coordenadas = json.load(f)
            
            logger.info(f"✅ Coordenadas carregadas: {len(self.coordenadas)} cidades")
            return len(self.coordenadas) > 0
            
        except Exception as e:
            logger.error(f"Erro ao carregar coordenadas: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def calcular_crescimento_cidade(self, arquivo_csv: str) -> float:
        """
        Calcula crescimento total da cidade
        
        Args:
            arquivo_csv: Arquivo de resultados da cidade
            
        Returns:
            float: Taxa de crescimento normalizada [-1, 1]
        """
        try:
            caminho = Path(arquivo_csv)
            if not caminho.exists():
                return 0.0
            
            dados_ano = defaultdict(list)
            
            with open(arquivo_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ano = int(row['ano'])
                    intensidade = float(row['intensidade_media'])
                    dados_ano[ano].append(intensidade)
            
            if len(dados_ano) < 2:
                return 0.0
            
            anos_ordenados = sorted(list(dados_ano.keys()))
            ano_primeiro = anos_ordenados[0]
            ano_ultimo = anos_ordenados[-1]
            
            media_primeiro = sum(dados_ano[ano_primeiro]) / len(dados_ano[ano_primeiro])
            media_ultimo = sum(dados_ano[ano_ultimo]) / len(dados_ano[ano_ultimo])
            
            if media_primeiro > 0:
                crescimento = (media_ultimo - media_primeiro) / media_primeiro
                return max(-1, min(1, crescimento))  # Normalizar para [-1, 1]
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Erro ao calcular crescimento: {e}")
            return 0.0
    
    def processar_todas_cidades(self, diretorio: str = '.') -> dict:
        """
        Processa crescimento de todas as cidades
        
        Args:
            diretorio: Diretório com arquivos resultados_*.csv
            
        Returns:
            dict: Crescimento por cidade
        """
        diretorio = Path(diretorio)
        
        for arquivo in diretorio.glob('resultados_*.csv'):
            # Extrair nome da cidade do arquivo
            nome_arquivo = arquivo.stem.replace('resultados_', '')
            
            # Calcular crescimento
            crescimento = self.calcular_crescimento_cidade(str(arquivo))
            self.crescimento_cidades[nome_arquivo] = crescimento
            
            logger.info(f"  {nome_arquivo}: {crescimento*100:+.2f}%")
        
        logger.info(f"✅ Processadas {len(self.crescimento_cidades)} cidades")
        return self.crescimento_cidades
    
    def obter_cor_crescimento(self, taxa: float) -> str:
        """
        Obtém cor baseada na taxa de crescimento
        
        Args:
            taxa: Taxa normalizada [-1, 1]
            
        Returns:
            str: Código hex da cor
        """
        if taxa < -0.05:
            # Azul (diminuição)
            if taxa < -0.5:
                return '#0033FF'  # Azul escuro
            else:
                return '#6699FF'  # Azul claro
        elif taxa > 0.05:
            # Vermelho (crescimento)
            if taxa > 0.5:
                return '#FF0000'  # Vermelho escuro
            else:
                return '#FF6666'  # Vermelho claro
        else:
            # Amarelo (estável)
            return '#FFDD00'  # Amarelo
    
    def gerar_geojson(self, arquivo_saida: str = 'mapa_crescimento.geojson') -> str:
        """
        Gera arquivo GeoJSON para visualização no mapa
        
        Args:
            arquivo_saida: Caminho do arquivo GeoJSON
            
        Returns:
            str: Caminho do arquivo salvo
        """
        features = []
        
        for cidade, crescimento in self.crescimento_cidades.items():
            # Encontrar coordenadas
            coord = self.coordenadas.get(cidade)
            if not coord:
                logger.warning(f"Coordenadas não encontradas para {cidade}")
                continue
            
            # Extrair lat/lon
            try:
                if isinstance(coord, dict):
                    lat = coord.get('latitude', coord.get('lat'))
                    lon = coord.get('longitude', coord.get('lon'))
                elif isinstance(coord, (list, tuple)) and len(coord) >= 2:
                    lat, lon = coord[0], coord[1]
                else:
                    continue
                
                cor = self.obter_cor_crescimento(crescimento)
                
                feature = {
                    "type": "Feature",
                    "properties": {
                        "cidade": cidade,
                        "crescimento": f"{crescimento*100:+.2f}%",
                        "taxa": crescimento,
                        "cor": cor,
                        "descricao": self._obter_descricao(crescimento)
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    }
                }
                
                features.append(feature)
            
            except Exception as e:
                logger.warning(f"Erro ao processar {cidade}: {e}")
                continue
        
        # Criar FeatureCollection
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        # Salvar arquivo
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ GeoJSON salvo: {arquivo_saida} ({len(features)} cidades)")
        return arquivo_saida
    
    def _obter_descricao(self, taxa: float) -> str:
        """Obtém descrição do crescimento"""
        if taxa < -0.05:
            return "Em decréscimo"
        elif taxa > 0.05:
            return "Em crescimento"
        else:
            return "Estável"
    
    def gerar_dados_api(self) -> dict:
        """
        Gera dados estruturados para API
        
        Returns:
            dict: Dados prontos para JavaScript
        """
        cidades_data = []
        
        for cidade, crescimento in self.crescimento_cidades.items():
            coord = self.coordenadas.get(cidade)
            if not coord:
                continue
            
            try:
                if isinstance(coord, dict):
                    lat = coord.get('latitude', coord.get('lat'))
                    lon = coord.get('longitude', coord.get('lon'))
                elif isinstance(coord, (list, tuple)) and len(coord) >= 2:
                    lat, lon = coord[0], coord[1]
                else:
                    continue
                
                cor = self.obter_cor_crescimento(crescimento)
                
                cidades_data.append({
                    'cidade': cidade,
                    'lat': lat,
                    'lon': lon,
                    'crescimento': round(crescimento * 100, 2),
                    'cor': cor,
                    'descricao': self._obter_descricao(crescimento)
                })
            
            except Exception as e:
                logger.warning(f"Erro ao processar {cidade}: {e}")
                continue
        
        return {
            'cidades': cidades_data,
            'total': len(cidades_data),
            'estatisticas': self._calcular_estatisticas()
        }
    
    def _calcular_estatisticas(self) -> dict:
        """Calcula estatísticas do crescimento"""
        if not self.crescimento_cidades:
            return {}
        
        valores = list(self.crescimento_cidades.values())
        crescimento = sum(1 for v in valores if v > 0.05)
        decrescimo = sum(1 for v in valores if v < -0.05)
        estavel = len(valores) - crescimento - decrescimo
        
        return {
            'total_cidades': len(valores),
            'em_crescimento': crescimento,
            'em_decrescimo': decrescimo,
            'estavel': estavel,
            'crescimento_medio': round(sum(valores) / len(valores) * 100, 2),
            'maior_crescimento': round(max(valores) * 100, 2),
            'maior_decrescimo': round(min(valores) * 100, 2)
        }
    
    def gerar_relatorio_html(self, arquivo_saida: str = 'mapa_crescimento.html') -> str:
        """Gera HTML com mapa interativo (usando Leaflet)"""
        dados = self.gerar_dados_api()
        dados_json = json.dumps(dados['cidades'], ensure_ascii=False)
        
        stats = dados['estatisticas']
        crescimento = stats.get('em_crescimento', 0)
        decrescimo = stats.get('em_decrescimo', 0)
        estavel = stats.get('estavel', 0)
        media = stats.get('crescimento_medio', 0)
        maximo = stats.get('maior_crescimento', 0)
        minimo = stats.get('maior_decrescimo', 0)
        
        html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa de Crescimento Luminoso</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .container { display: flex; height: 100vh; }
        #mapa { flex: 1; background: #e0e0e0; }
        .sidebar { width: 350px; background: white; box-shadow: -2px 0 10px rgba(0,0,0,0.1); overflow-y: auto; padding: 20px; }
        .sidebar h1 { font-size: 18px; color: #333; margin-bottom: 20px; }
        .legenda { background: #f9f9f9; border-left: 4px solid #667eea; padding: 15px; margin-bottom: 20px; border-radius: 4px; }
        .legenda-item { display: flex; align-items: center; margin-bottom: 10px; font-size: 14px; }
        .legenda-cor { width: 20px; height: 20px; border-radius: 50%; margin-right: 10px; border: 1px solid #999; }
        .stats { background: #f0f3ff; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
        .stat-item { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px; }
        .stat-label { color: #666; }
        .stat-value { font-weight: bold; color: #333; }
        .cidades-lista { font-size: 12px; }
        .cidade-item { padding: 10px; border-left: 4px solid #ccc; margin-bottom: 8px; cursor: pointer; background: #fafafa; border-radius: 4px; transition: all 0.3s; }
        .cidade-item:hover { background: #f0f0f0; }
        .cidade-nome { font-weight: bold; color: #333; margin-bottom: 3px; }
        .cidade-crescimento { font-size: 11px; color: #666; }
        .popup-titulo { font-weight: bold; font-size: 14px; margin-bottom: 5px; }
        .popup-crescimento { font-size: 13px; font-weight: bold; }
        .popup-descricao { font-size: 12px; color: #666; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h1>Cidades</h1>
            <div class="legenda">
                <div class="legenda-item">
                    <div class="legenda-cor" style="background: #FF0000;"></div>
                    <span>Crescimento</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background: #FFDD00;"></div>
                    <span>Estável</span>
                </div>
                <div class="legenda-item">
                    <div class="legenda-cor" style="background: #0033FF;"></div>
                    <span>Diminuição</span>
                </div>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-label">Total:</span>
                    <span class="stat-value" style="color: #667eea;">""" + str(len(dados['cidades'])) + """</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Crescimento:</span>
                    <span class="stat-value" style="color: #FF0000;">+""" + str(crescimento) + """</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Decréscimo:</span>
                    <span class="stat-value" style="color: #0033FF;">-""" + str(decrescimo) + """</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Estável:</span>
                    <span class="stat-value" style="color: #FFAA00;">""" + str(estavel) + """</span>
                </div>
                <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
                <div class="stat-item">
                    <span class="stat-label">Média:</span>
                    <span class="stat-value">""" + f"{media:+.2f}" + """%</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Máximo:</span>
                    <span class="stat-value" style="color: #FF0000;">""" + f"{maximo:+.2f}" + """%</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Mínimo:</span>
                    <span class="stat-value" style="color: #0033FF;">""" + f"{minimo:+.2f}" + """%</span>
                </div>
            </div>
            <div id="cidades-lista" class="cidades-lista"></div>
        </div>
        <div id="mapa"></div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <script>
        const dadosCidades = """ + dados_json + """;
        const mapa = L.map('mapa').setView([-26.8, -49.3], 9);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(mapa);
        const marcadores = {};
        dadosCidades.forEach(cidade => {
            const marcador = L.circleMarker([cidade.lat, cidade.lon], {
                radius: 10,
                fillColor: cidade.cor,
                color: '#333',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            }).addTo(mapa);
            marcador.bindPopup(`
                <div class="popup-titulo">${cidade.cidade}</div>
                <div class="popup-crescimento">${cidade.crescimento > 0 ? '+' : ''}${cidade.crescimento}%</div>
                <div class="popup-descricao">${cidade.descricao}</div>
            `);
            marcadores[cidade.cidade] = marcador;
        });
        const lista = document.getElementById('cidades-lista');
        dadosCidades.sort((a, b) => b.crescimento - a.crescimento).forEach(cidade => {
            const div = document.createElement('div');
            div.className = 'cidade-item';
            div.style.borderLeftColor = cidade.cor;
            div.innerHTML = `
                <div class="cidade-nome">${cidade.cidade}</div>
                <div class="cidade-crescimento">${cidade.crescimento > 0 ? '+' : ''}${cidade.crescimento}% - ${cidade.descricao}</div>
            `;
            div.onclick = () => {
                const marcador = marcadores[cidade.cidade];
                if (marcador) {
                    mapa.setView([cidade.lat, cidade.lon], 12);
                    marcador.openPopup();
                }
            };
            lista.appendChild(div);
        });
    </script>
</body>
</html>
"""
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✅ HTML salvo: {arquivo_saida}")
        return arquivo_saida
    
    def calcular_crescimento_cidade_unica(self, nome_cidade: str) -> dict:
        """
        Calcula crescimento para uma cidade específica
        
        Args:
            nome_cidade: Nome da cidade (formato usado em resultados_*.csv)
            
        Returns:
            dict: Dados da cidade com crescimento
        """
        # Encontrar o arquivo CSV com qualquer variação de nome
        arquivo_csv_str = self.encontrar_arquivo_csv(nome_cidade)
        
        if not arquivo_csv_str:
            logger.warning(f"Arquivo de resultados não encontrado para: {nome_cidade}")
            return {}
        
        arquivo_csv = Path(arquivo_csv_str)
        
        try:
            dados_por_ano = {}
            with open(arquivo_csv, 'r', encoding='utf-8') as f:
                leitor = csv.DictReader(f)
                for linha in leitor:
                    ano = int(linha.get('ano', 0))
                    intensidade = float(linha.get('intensidade_media', 0))
                    if ano not in dados_por_ano:
                        dados_por_ano[ano] = []
                    dados_por_ano[ano].append(intensidade)
            
            if len(dados_por_ano) < 2:
                return {}
            
            anos_ordenados = sorted(dados_por_ano.keys())
            primeira_intensidade = sum(dados_por_ano[anos_ordenados[0]]) / len(dados_por_ano[anos_ordenados[0]])
            ultima_intensidade = sum(dados_por_ano[anos_ordenados[-1]]) / len(dados_por_ano[anos_ordenados[-1]])
            
            if primeira_intensidade == 0:
                crescimento = 0
            else:
                crescimento = (ultima_intensidade - primeira_intensidade) / primeira_intensidade
            
            # Formatar nome da cidade para exibição e procura de coordenadas
            nome_exibicao = nome_cidade.replace('_', ' ')
            
            # Remover sufixos (recorte, recortado, etc.) para encontrar coordenadas
            nome_busca = nome_exibicao.lower()
            # IMPORTANTE: remover '_recortes' ANTES de '_recorte' para evitar deixar 's'
            for sufixo in ['recortes', 'recorte', 'recortado', 'reprojetado', 'reprojet', 'noturno', 'noturna']:
                nome_busca = nome_busca.replace(f' {sufixo}', '').replace(f'_{sufixo}', '')
            
            # Procurar a coordenada usando o nome limpo
            coordenada = None
            for chave in self.coordenadas.keys():
                if chave.lower() == nome_busca or chave.lower().replace(' ', '_') == nome_busca.replace(' ', '_'):
                    coordenada = self.coordenadas[chave]
                    break
            
            if not coordenada:
                logger.warning(f"Coordenada não encontrada para {nome_cidade} (buscado: {nome_busca})")
                return {}
            
            if isinstance(coordenada, list):
                lat, lon = coordenada[0], coordenada[1]
            else:
                lat = coordenada.get('latitude', coordenada.get('lat'))
                lon = coordenada.get('longitude', coordenada.get('lon'))
            
            cor = self.obter_cor_crescimento(crescimento)
            
            return {
                'nome': nome_exibicao,
                'lat': lat,
                'lon': lon,
                'crescimento': round(crescimento * 100, 2),
                'cor': cor,
                'descricao': self._obter_descricao(crescimento),
                'intensidade_inicial': round(primeira_intensidade, 2),
                'intensidade_final': round(ultima_intensidade, 2),
                'anos': f"{anos_ordenados[0]}-{anos_ordenados[-1]}"
            }
        
        except Exception as e:
            logger.error(f"Erro ao calcular crescimento de {nome_cidade}: {e}")
            return {}
    
    def _binarizar_imagem(self, imagem: np.ndarray) -> np.ndarray:
        """
        Realça contraste e detalhes com stretching agressivo.
        Mostra áreas com luz de forma clara e visível.
        
        Args:
            imagem: Array numpy com dados da imagem
            
        Returns:
            np.ndarray: Imagem com contraste agressivo
        """
        try:
            # Normalizar para 0-255
            if imagem.dtype == np.float32 or imagem.dtype == np.float64:
                valid_mask = ~np.isnan(imagem) & (imagem != 0)
                if np.any(valid_mask):
                    valid_data = imagem[valid_mask]
                    # Usar percentis extremos para máximo contraste
                    img_min = np.percentile(valid_data, 1)
                    img_max = np.percentile(valid_data, 99)
                    if img_max > img_min:
                        imagem_norm = (imagem - img_min) / (img_max - img_min) * 255
                        imagem_norm = np.clip(imagem_norm, 0, 255)
                    else:
                        imagem_norm = np.zeros_like(imagem)
                else:
                    imagem_norm = np.zeros_like(imagem)
            else:
                imagem_norm = np.clip(imagem, 0, 255)
            
            imagem_uint8 = imagem_norm.astype(np.uint8)
            
            # Aplicar curva não-linear para realçar áreas com luz
            # Usar power law (gamma correction) para intensificar luzes
            imagem_gamma = np.power(imagem_uint8 / 255.0, 0.4) * 255
            imagem_gamma = np.uint8(np.clip(imagem_gamma, 0, 255))
            
            # Stretching final MUITO agressivo
            # Separar em dark e light
            media = np.mean(imagem_gamma[imagem_gamma > 0]) if np.any(imagem_gamma > 0) else 100
            
            imagem_final = np.where(imagem_gamma > media * 0.5,
                                   np.uint8(np.clip(imagem_gamma * 2.0, 0, 255)),  # 2x mais branco
                                   np.uint8(np.clip(imagem_gamma * 0.3, 0, 255)))   # 3x mais preto
            
            logger.debug(f"Contraste agressivo aplicado: gamma 0.4 + stretching 2x/3x")
            return imagem_final
            
        except Exception as e:
            logger.warning(f"Erro na normalização: {e}")
            return np.zeros_like(imagem, dtype=np.uint8)
            
        except Exception as e:
            logger.warning(f"Erro na binarização, usando threshold 127: {e}")
            # Fallback: usar threshold simples
            try:
                if imagem.dtype == np.float32 or imagem.dtype == np.float64:
                    threshold = np.median(imagem[imagem > 0]) if np.any(imagem > 0) else 0.5
                else:
                    threshold = 127
                
                return (imagem > threshold).astype(np.uint8) * 255
            except:
                # Se tudo falhar, retornar imagem vazia
                return np.zeros_like(imagem, dtype=np.uint8)
    
    def gerar_timelapse_cidade(self, nome_cidade: str, caminho_pasta_recorte: str, arquivo_saida: str = None) -> str:
        """
        Gera timelapse HTML das imagens da cidade com overlay de crescimento colorido
        
        Args:
            nome_cidade: Nome da cidade
            caminho_pasta_recorte: Caminho completo da pasta com imagens recortadas
            arquivo_saida: Arquivo HTML de saída
            
        Returns:
            str: Caminho do arquivo gerado ou None
        """
        if arquivo_saida is None:
            arquivo_saida = DIRETORIO_TRABALHO / f'timelapse_{nome_cidade}.html'
        
        # Obter dados da cidade
        dados_cidade = self.calcular_crescimento_cidade_unica(nome_cidade)
        if not dados_cidade:
            logger.error(f"Nenhum dado encontrado para {nome_cidade}")
            return None
        
        # Encontrar imagens TIF na pasta (procurar recursivamente)
        caminho_pasta = Path(caminho_pasta_recorte)
        if not caminho_pasta.exists():
            logger.error(f"Pasta não encontrada: {caminho_pasta}")
            return None
        
        # Procurar por imagens TIF recursivamente
        imagens_tif_todas = sorted(caminho_pasta.glob('**/*.tif'))
        if not imagens_tif_todas:
            logger.warning(f"Nenhuma imagem TIF encontrada em {caminho_pasta}")
            return None
        
        # FILTRAR APENAS IMAGENS DE MÊSES 12 (DEZEMBRO)
        # Padrão de nome: cidade_ano_mes.tif (ex: balneario_camboriu_2014_12.tif)
        imagens_tif = []
        for img_path in imagens_tif_todas:
            try:
                # Extrair mês do nome do arquivo (último elemento antes da extensão)
                partes = img_path.stem.split('_')
                mes = partes[-1] if len(partes) > 0 else '0'
                
                # Manter apenas imagens do mês 12
                if mes == '12':
                    imagens_tif.append(img_path)
                    logger.debug(f"✅ Imagem de dezembro encontrada: {img_path.name}")
            except Exception as e:
                logger.debug(f"Erro ao processar nome do arquivo: {img_path.name} - {e}")
                continue
        
        if not imagens_tif:
            logger.warning(f"Nenhuma imagem TIF de dezembro (mês 12) encontrada em {caminho_pasta}")
            logger.info(f"   Total de TIFs encontrados: {len(imagens_tif_todas)}")
            return None
        
        logger.info(f"✅ {len(imagens_tif)} imagens de DEZEMBRO encontradas para timelapse")
        
        # Carregar primeira e última imagem para criar mapa de crescimento
        imagem_inicio = None
        imagem_fim = None
        mapa_crescimento = None
        
        try:
            import rasterio
            import numpy as np
            
            # Ler primeira e última imagem
            with rasterio.open(imagens_tif[0]) as src:
                imagem_inicio = src.read(1).astype(np.float32)
            
            with rasterio.open(imagens_tif[-1]) as src:
                imagem_fim = src.read(1).astype(np.float32)
            
            # Calcular crescimento
            mapa_crescimento = self._calcular_mapa_crescimento(imagem_inicio, imagem_fim)
            logger.info(f"✅ Mapa de crescimento calculado")
            
        except Exception as e:
            logger.warning(f"Erro ao calcular mapa de crescimento: {e}")
            mapa_crescimento = None
        
        # Converter imagens para base64 com overlay de crescimento
        imagens_base64 = []
        
        # ADICIONAR MAPA DE CRESCIMENTO COMO PRIMEIRA IMAGEM
        if mapa_crescimento is not None and imagem_inicio is not None and imagem_fim is not None:
            try:
                logger.info("🎨 Criando imagem visual de crescimento...")
                from PIL import Image
                
                # O mapa já é uint8, agora é só converter para imagem
                crescimento_img = Image.fromarray(mapa_crescimento, mode='L')
                crescimento_img = crescimento_img.convert('RGB')
                crescimento_img = crescimento_img.resize((4096, 3072), Image.Resampling.LANCZOS)
                
                # Salvar mapa de crescimento como primeira imagem
                buffer = BytesIO()
                crescimento_img.save(buffer, format='PNG', optimize=False, quality=95)
                buffer.seek(0)
                
                img_b64 = base64.b64encode(buffer.getvalue()).decode()
                imagens_base64.append({
                    'nome': '📈_CRESCIMENTO_2014-2024.png',
                    'data': f'data:image/png;base64,{img_b64}'
                })
                logger.info(f"✅ Mapa de crescimento adicionado como primeira imagem (tamanho: {len(img_b64)} bytes)")
            except Exception as e:
                logger.warning(f"Erro ao criar mapa de crescimento visual: {e}")
        
        try:
            logger.info(f"Total de imagens TIF encontradas: {len(imagens_tif)}")
            # Tentar usar rasterio para GeoTIFF
            try:
                import rasterio
                import numpy as np
                from PIL import Image, ImageEnhance
                
                logger.info(f"Processando {len(imagens_tif)} imagens de dezembro com rasterio (uma por ano)...")
                for idx, img_path in enumerate(imagens_tif):
                    try:
                        logger.debug(f"Processando imagem {idx+1}: {img_path.name}")
                        # Abrir com rasterio (suporta GeoTIFF com floating point)
                        with rasterio.open(img_path) as src:
                            # Ler primeira banda
                            band = src.read(1)
                            
                            # BINARIZAR A IMAGEM (converter para preto e branco)
                            band_binario = self._binarizar_imagem(band)
                            
                            # Converter para imagem PIL em modo L (escala de cinza)
                            img = Image.fromarray(band_binario, mode='L')
                            
                            # Converter para RGB para consistência com overlay
                            img = img.convert('RGB')
                            
                            # Redimensionar para Ultra HD (4K)
                            img = img.resize((4096, 3072), Image.Resampling.LANCZOS)
                            
                            # Converter para PNG em memória com máxima qualidade
                            buffer = BytesIO()
                            img.save(buffer, format='PNG', optimize=False, quality=95)
                            buffer.seek(0)
                            
                            # Codificar em base64
                            img_b64 = base64.b64encode(buffer.getvalue()).decode()
                            imagens_base64.append({
                                'nome': img_path.name,
                                'data': f'data:image/png;base64,{img_b64}'
                            })
                            logger.debug(f"✅ Imagem binária {idx+1} processada (tamanho: {len(img_b64)} bytes)")
                            
                    except Exception as e:
                        logger.warning(f"Erro ao processar com rasterio {img_path.name}: {e}")
                        continue
                        
            except ImportError:
                # Fallback para PIL se rasterio não estiver disponível
                from PIL import Image, ImageEnhance
                import numpy as np
                
                for idx, img_path in enumerate(imagens_tif):
                    try:
                        img = Image.open(img_path)
                        img_array = np.array(img)
                        
                        # Converter para escala de cinza se necessário
                        if len(img_array.shape) == 3:
                            img_array = np.mean(img_array[:,:,:3], axis=2)
                        
                        # BINARIZAR A IMAGEM
                        band_binario = self._binarizar_imagem(img_array.astype(np.float32))
                        
                        # Criar imagem PIL em escala de cinza
                        img = Image.fromarray(band_binario.astype(np.uint8), mode='L')
                        img = img.convert('RGB')
                        
                        # Redimensionar para tamanho maior
                        img = img.resize((1800, 1350), Image.Resampling.LANCZOS)
                        
                        buffer = BytesIO()
                        img.save(buffer, format='PNG')
                        buffer.seek(0)
                        
                        img_b64 = base64.b64encode(buffer.getvalue()).decode()
                        imagens_base64.append({
                            'nome': img_path.name,
                            'data': f'data:image/png;base64,{img_b64}'
                        })
                        logger.debug(f"✅ Imagem binária (PIL) {idx+1} processada")
                        
                    except Exception as e:
                        logger.warning(f"Erro ao processar com PIL {img_path.name}: {e}")
                        continue
        
        except ImportError:
            logger.warning("PIL não disponível, criando timelapse com placeholder")
            # Usar placeholder se PIL não estiver disponível
            imagens_base64 = [{'nome': img.name, 'data': 'placeholder'} for img in imagens_tif]
        
        if not imagens_base64:
            logger.error("Nenhuma imagem pode ser processada")
            return None
        
        # Dados JSON para o timelapse
        logger.info(f"Total de imagens coletadas para timelapse: {len(imagens_base64)}")
        
        imagens_json = json.dumps(imagens_base64, ensure_ascii=False)
        dados_json = json.dumps({
            'cidade': dados_cidade['nome'],
            'crescimento': dados_cidade['crescimento'],
            'intensidade_inicial': dados_cidade['intensidade_inicial'],
            'intensidade_final': dados_cidade['intensidade_final'],
            'anos': dados_cidade['anos'],
            'cor_crescimento': '#FF4444' if dados_cidade['crescimento'] >= 5 else '#FFD700'
        }, ensure_ascii=False)
        
        # Criar HTML do timelapse com encoding correto
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Timelapse - {dados_cidade['nome']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a1a; }}
        
        .container {{
            display: flex;
            flex-direction: column;
            height: 100vh;
            background: #0a0a0a;
        }}
        
        .viewer {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            background: #222;
            overflow: hidden;
        }}
        
        .imagem-container {{
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
        }}
        
        .imagem-container img {{
            max-width: 100%;
            max-height: 100%;
            width: auto;
            height: auto;
            object-fit: contain;
            display: block;
            image-rendering: crisp-edges;
            filter: contrast(1.15);
        }}
        
        .overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(ellipse at center, rgba(255, 100, 100, 0.3) 0%, transparent 70%);
            pointer-events: none;
        }}
        
        .info-panel {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 100;
            max-width: 300px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        .info-panel h2 {{ margin: 0 0 10px 0; color: #333; font-size: 16px; }}
        .info-panel p {{ margin: 5px 0; color: #666; font-size: 13px; }}
        
        .growth-label {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 8px;
            font-size: 12px;
        }}
        
        .growth-label.crescimento {{ background-color: #FF4444; color: white; }}
        .growth-label.estavel {{ background-color: #FFD700; color: #333; }}
        
        .controls {{
            background: #222;
            padding: 20px;
            border-top: 1px solid #444;
        }}
        
        .control-group {{
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        button {{
            background: #FF4444;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }}
        
        button:hover {{ background: #FF6666; }}
        button:disabled {{ background: #888; cursor: not-allowed; }}
        
        input[type="range"] {{
            flex: 1;
            height: 6px;
            border-radius: 3px;
            background: #444;
            outline: none;
            -webkit-appearance: none;
        }}
        
        input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #FF4444;
            cursor: pointer;
        }}
        
        input[type="range"]::-moz-range-thumb {{
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #FF4444;
            cursor: pointer;
            border: none;
        }}
        
        .tempo-display {{
            color: #fff;
            font-size: 14px;
            min-width: 100px;
            text-align: center;
        }}
        
        .legenda {{
            color: #aaa;
            font-size: 12px;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #444;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="viewer">
            <div class="imagem-container">
                <img id="imagemPrincipal" src="" alt="Timelapse">
                <div class="overlay"></div>
            </div>
            <div class="info-panel">
                <h2 id="nomeApp"></h2>
                <p><strong>Período:</strong> <span id="periodoApp"></span></p>
                <p><strong>Intensidade 2014:</strong> <span id="intensidadeInicio"></span></p>
                <p><strong>Intensidade 2024:</strong> <span id="intensidadeFim"></span></p>
                <div id="labelCrescimento" class="growth-label"></div>
            </div>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <button id="btnPlay">▶ Play</button>
                <button id="btnPause">⏸ Pausa</button>
                <input type="range" id="sliderTempo" min="0" max="100" value="0">
                <span class="tempo-display"><span id="frameAtual">1</span> / <span id="totalFrames">1</span></span>
            </div>
            <div class="legenda">
                <strong>Avermelhado</strong> = Crescimento de intensidade luminosa<br>
                <strong>Escala de Cinza</strong> = Intensidade luminosa original
            </div>
        </div>
    </div>
    
    <script>
        const dados = {dados_json};
        const imagens = {imagens_json};
        
        let indiceAtual = 0;
        let tocando = false;
        let intervalo = null;
        
        const imgPrincipal = document.getElementById('imagemPrincipal');
        const sliderTempo = document.getElementById('sliderTempo');
        const btnPlay = document.getElementById('btnPlay');
        const btnPause = document.getElementById('btnPause');
        const frameAtual = document.getElementById('frameAtual');
        const totalFrames = document.getElementById('totalFrames');
        
        // Inicializar informações
        document.getElementById('nomeApp').textContent = dados.cidade;
        document.getElementById('periodoApp').textContent = dados.anos;
        document.getElementById('intensidadeInicio').textContent = dados.intensidade_inicial;
        document.getElementById('intensidadeFim').textContent = dados.intensidade_final;
        
        const labelCrescimento = document.getElementById('labelCrescimento');
        labelCrescimento.className = 'growth-label ' + (dados.crescimento >= 5 ? 'crescimento' : 'estavel');
        labelCrescimento.textContent = (dados.crescimento >= 5 ? '📈 ' : '⚖️ ') + 
                                      Math.abs(dados.crescimento).toFixed(1) + '% ' +
                                      (dados.crescimento >= 5 ? 'CRESCIMENTO' : 'VARIAÇÃO');
        
        totalFrames.textContent = imagens.length;
        sliderTempo.max = imagens.length - 1;
        
        function mostrarFrame(indice) {{
            if (indice < 0 || indice >= imagens.length) return;
            
            indiceAtual = indice;
            const imagem = imagens[indice];
            
            if (imagem.data !== 'placeholder') {{
                imgPrincipal.src = imagem.data;
            }} else {{
                imgPrincipal.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><rect width="800" height="600" fill="%23333"/><text x="400" y="300" fill="%23fff" text-anchor="middle" font-size="24">Imagem não disponível</text></svg>';
            }}
            
            sliderTempo.value = indice;
            frameAtual.textContent = indice + 1;
        }}
        
        function play() {{
            if (tocando) return;
            tocando = true;
            btnPlay.disabled = true;
            btnPause.disabled = false;
            
            intervalo = setInterval(() => {{
                if (indiceAtual < imagens.length - 1) {{
                    mostrarFrame(indiceAtual + 1);
                }} else {{
                    clearInterval(intervalo);
                    tocando = false;
                    btnPlay.disabled = false;
                    btnPause.disabled = true;
                }}
            }}, 500);
        }}
        
        function pausa() {{
            tocando = false;
            btnPlay.disabled = false;
            btnPause.disabled = true;
            if (intervalo) clearInterval(intervalo);
        }}
        
        btnPlay.addEventListener('click', play);
        btnPause.addEventListener('click', pausa);
        sliderTempo.addEventListener('input', (e) => {{
            pausa();
            mostrarFrame(parseInt(e.target.value));
        }});
        
        // Carregar primeiro frame
        mostrarFrame(0);
    </script>
</body>
</html>"""
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✅ Timelapse gerado para {nome_cidade}: {arquivo_saida}")
        return str(arquivo_saida)
    
    def _gerar_pontos_heatmap(self, arquivo_csv: str, dados_cidade: dict) -> list:
        """Gera lista de pontos de heatmap a partir dos dados de intensidade do CSV"""
        pontos = []
        try:
            with open(arquivo_csv) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        ano = int(row['ano'])
                        intensidade = float(row['intensidade_media'])
                        
                        # Usar coordenadas da cidade com pequeno offset para cada ano
                        # Simula pontos na área da cidade
                        lat = dados_cidade['lat'] + (intensidade - 0.5) * 0.001
                        lon = dados_cidade['lon'] + (intensidade - 0.5) * 0.001
                        
                        # Intensidade do heatmap (0-1)
                        peso = max(0, min(1, intensidade))
                        
                        pontos.append([lat, lon, peso])
                    except (ValueError, KeyError):
                        continue
        except Exception as e:
            logger.error(f"Erro ao gerar pontos de heatmap: {e}")
            # Retornar um ponto padrão se houver erro
            lat = dados_cidade['lat']
            lon = dados_cidade['lon']
            pontos = [[lat, lon, 0.5]]
        
        return pontos
    
    def gerar_relatorio_html_cidade(self, nome_cidade: str, arquivo_saida: str = None) -> str:
        """Gera mapa HTML recortado apenas da cidade com heatmap de crescimento colorido"""
        if arquivo_saida is None:
            arquivo_saida = DIRETORIO_TRABALHO / f'mapa_{nome_cidade}.html'
        
        dados_cidade = self.calcular_crescimento_cidade_unica(nome_cidade)
        if not dados_cidade:
            logger.error(f"Nenhum dado encontrado para {nome_cidade}")
            return None
        
        # Obter dados de intensidade por período para criar heatmap
        arquivo_csv_str = self.encontrar_arquivo_csv(nome_cidade)
        if not arquivo_csv_str:
            return None
        
        # Ler dados de intensidade e gerar pontos de heatmap
        pontos_heatmap = self._gerar_pontos_heatmap(arquivo_csv_str, dados_cidade)
        
        nome_display = dados_cidade['nome']
        lat = dados_cidade['lat']
        lon = dados_cidade['lon']
        
        # Criar JSON dos pontos de heatmap
        dados_heatmap_json = json.dumps(pontos_heatmap, ensure_ascii=False)
        
        # Construir HTML do mapa recortado com heatmap
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mapa de Crescimento - ''' + nome_display + '''</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-heatmap/1.0.4/leaflet-heatmap.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        
        #mapa { width: 100%; height: 100vh; background: #E8E8E8; }
        
        .header {
            position: absolute;
            top: 10px;
            left: 50px;
            background: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            z-index: 1000;
            max-width: 400px;
            font-size: 16px;
            color: #333;
        }
        
        .header h2 {
            margin: 0 0 8px 0;
            color: #222;
            font-size: 18px;
        }
        
        .header p {
            margin: 4px 0;
            color: #666;
            font-size: 13px;
        }
        
        .info-crescimento {
            display: inline-block;
            padding: 8px 12px;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 8px;
            font-size: 14px;
        }
        
        .info-crescimento.crescimento { background-color: #FF4444; color: white; }
        .info-crescimento.estavel { background-color: #FFD700; color: #333; }
        
        .legenda {
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            z-index: 1000;
            font-size: 13px;
        }
        
        .legenda h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        
        .gradiente {
            display: flex;
            height: 30px;
            margin: 10px 0;
            border-radius: 4px;
            background: linear-gradient(to right, #FFD700 0%, #FF8800 50%, #FF4444 100%);
            border: 1px solid #999;
        }
        
        .legenda-label {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            margin-top: 5px;
            color: #666;
        }
    </style>
</head>
<body>
    <div id="mapa"></div>
    <div class="header">
        <h2>''' + nome_display + '''</h2>
        <p><strong>Intensidade de Luz</strong></p>
        <p>2014: ''' + str(dados_cidade['intensidade_inicial']) + ''' → 2024: ''' + str(dados_cidade['intensidade_final']) + '''</p>
        <div class="info-crescimento ''' + ('crescimento' if dados_cidade['crescimento'] >= 5 else 'estavel') + '''">
            ''' + ('📈 +' if dados_cidade['crescimento'] >= 5 else '⚖️ ') + str(abs(dados_cidade['crescimento'])) + '''% 
            ''' + ('CRESCIMENTO' if dados_cidade['crescimento'] >= 5 else 'VARIAÇÃO') + '''
        </div>
    </div>
    
    <div class="legenda">
        <h4>Intensidade Luminosa</h4>
        <div class="gradiente"></div>
        <div class="legenda-label">
            <span>Baixa (Amarelo)</span>
            <span>Alta (Vermelho)</span>
        </div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/heatmap.js/2.0.5/heatmap.min.js"></script>
    <script>
        // Dados da cidade
        const latitude = ''' + str(lat) + ''';
        const longitude = ''' + str(lon) + ''';
        const nomeCidade = "''' + nome_display + '''";
        const pontosHeatmap = ''' + dados_heatmap_json + ''';
        
        // Criar mapa RECORTADO apenas na cidade
        const mapa = L.map('mapa').setView([latitude, longitude], 13);
        
        // Camada base
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap',
            maxZoom: 18,
            minZoom: 12,
            zIndex: 1
        }).addTo(mapa);
        
        // Adicionar heatmap dos pontos de crescimento
        if (pontosHeatmap.length > 0) {
            L.heatLayer(pontosHeatmap, {
                radius: 35,
                blur: 25,
                maxZoom: 17,
                gradient: {0.0: '#FFD700', 0.5: '#FF8800', 1.0: '#FF4444'},
                minOpacity: 0.3,
                max: 100
            }).addTo(mapa);
        }
        
        // Limitar view apenas à cidade
        const bounds = L.latLngBounds(
            [latitude - 0.08, longitude - 0.08],
            [latitude + 0.08, longitude + 0.08]
        );
        mapa.setMaxBounds(bounds.pad(0.2));
        mapa.fitBounds(bounds);
    </script>
</body>
</html>'''
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✅ Mapa HTML com heatmap gerado para {nome_cidade}: {arquivo_saida}")
        return str(arquivo_saida)
    
    def _calcular_mapa_crescimento(self, imagem_inicio, imagem_fim):
        """
        Calcula mapa visual de crescimento (subtração) entre duas imagens.
        Cria uma imagem que mostra EXATAMENTE onde a luz cresceu.
        
        Returns:
            ndarray: Imagem com crescimento realçado (escala de cinza)
        """
        try:
            import numpy as np
            from PIL import Image
            
            # Garantir tipos iguais
            imagem_inicio = imagem_inicio.astype(np.float32)
            imagem_fim = imagem_fim.astype(np.float32)
            
            # Garantir que as imagens têm o mesmo tamanho
            if imagem_inicio.shape != imagem_fim.shape:
                logger.warning(f"Redimensionando segunda imagem para {imagem_inicio.shape}")
                img_fim_pil = Image.fromarray(np.uint8(np.clip(imagem_fim, 0, 255)))
                img_fim_pil = img_fim_pil.resize((imagem_inicio.shape[1], imagem_inicio.shape[0]), Image.Resampling.BILINEAR)
                imagem_fim = np.array(img_fim_pil).astype(np.float32)
            
            # Normalizar ambas para 0-1 para comparação justa
            def normalizar(img):
                valid = img[(~np.isnan(img)) & (img != 0)]
                if len(valid) > 0:
                    vmin, vmax = np.percentile(valid, [1, 99])
                    if vmax > vmin:
                        img = (img - vmin) / (vmax - vmin)
                    else:
                        img = np.zeros_like(img)
                return np.clip(img, 0, 1)
            
            imagem_inicio = normalizar(imagem_inicio)
            imagem_fim = normalizar(imagem_fim)
            
            # CALCULAR CRESCIMENTO = última - primeira
            crescimento = imagem_fim - imagem_inicio
            
            # Amplificar com power law para visualizar melhor
            crescimento_pos = np.maximum(crescimento, 0)  # Apenas crescimento positivo
            crescimento_amplif = np.power(crescimento_pos, 0.5) * 2  # Amplificar
            crescimento_amplif = np.clip(crescimento_amplif, 0, 1)
            
            # Converter para 0-255
            mapa_crescimento = (crescimento_amplif * 255).astype(np.uint8)
            
            logger.info(f"✅ Mapa de crescimento calculado: min={mapa_crescimento.min()}, max={mapa_crescimento.max()}, média={mapa_crescimento[mapa_crescimento>0].mean():.1f}")
            return mapa_crescimento
            
        except Exception as e:
            logger.error(f"Erro ao calcular mapa de crescimento: {e}")
            return None
