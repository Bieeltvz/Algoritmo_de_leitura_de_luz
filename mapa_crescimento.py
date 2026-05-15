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

# Definir diretório de trabalho
DIRETORIO_TRABALHO = Path(__file__).parent.absolute()
os.chdir(DIRETORIO_TRABALHO)


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
        
        Args:
            nome_cidade: Nome da cidade
            
        Returns:
            str: Caminho do arquivo CSV se encontrado, '' caso contrário
        """
        try:
            # Padrões possíveis para o arquivo CSV
            padroes = [
                f'resultados_{nome_cidade}.csv',  # Sem sufixo
                f'resultados_{nome_cidade}_recorte.csv',  # Com _recorte
                f'resultados_{nome_cidade}_Recorte.csv',  # Com _Recorte
                f'resultados_{nome_cidade}_recortes.csv',  # Com _recortes
                f'resultados_{nome_cidade}_Recortes.csv',  # Com _Recortes
                f'resultados_{nome_cidade}_RECORTADO.csv',  # Com _RECORTADO
            ]
            
            for padrao in padroes:
                arquivo = DIRETORIO_TRABALHO / padrao
                if arquivo.exists():
                    logger.info(f"✅ Arquivo encontrado: {padrao}")
                    return str(arquivo)
            
            # Se não encontrar com padrões, procura por qualquer arquivo com parte do nome
            logger.warning(f"Nenhum padrão exato encontrado para {nome_cidade}, procurando por padrão...")
            for arquivo in DIRETORIO_TRABALHO.glob('resultados_*.csv'):
                if nome_cidade.lower() in arquivo.name.lower():
                    logger.info(f"✅ Arquivo encontrado por padrão: {arquivo.name}")
                    return str(arquivo)
            
            logger.warning(f"❌ Nenhum arquivo de resultados encontrado para {nome_cidade}")
            return ''
            
        except Exception as e:
            logger.error(f"Erro ao procurar arquivo CSV: {e}")
            return ''
        
    def carregar_coordenadas(self, arquivo_json: str = 'coordenadas_cidades_completas_nominatim.json') -> bool:
        """
        Carrega coordenadas das cidades
        
        Args:
            arquivo_json: Arquivo com coordenadas
            
        Returns:
            bool: Sucesso na leitura
        """
        try:
            caminho = Path(arquivo_json)
            if not caminho.exists():
                logger.warning(f"Arquivo não encontrado: {arquivo_json}")
                return False
            
            with open(arquivo_json, 'r', encoding='utf-8') as f:
                self.coordenadas = json.load(f)
            
            logger.info(f"✅ Coordenadas carregadas: {len(self.coordenadas)} cidades")
            return len(self.coordenadas) > 0
            
        except Exception as e:
            logger.error(f"Erro ao carregar coordenadas: {e}")
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
            for sufixo in ['recorte', 'recortes', 'recortado', 'reprojetado', 'noturno', 'noturna', 'reprojet']:
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
        imagens_tif = sorted(caminho_pasta.glob('**/*.tif'))
        if not imagens_tif:
            logger.warning(f"Nenhuma imagem TIF encontrada em {caminho_pasta}")
            return None
        
        logger.info(f"✅ {len(imagens_tif)} imagens encontradas para timelapse")
        
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
        try:
            logger.info(f"Total de imagens TIF encontradas: {len(imagens_tif)}")
            # Tentar usar rasterio para GeoTIFF
            try:
                import rasterio
                import numpy as np
                from PIL import Image, ImageEnhance
                
                logger.info(f"Processando {min(24, len(imagens_tif))} imagens com rasterio...")
                for idx, img_path in enumerate(imagens_tif[:24]):  # Limitar a 24 imagens
                    try:
                        logger.debug(f"Processando imagem {idx+1}: {img_path.name}")
                        # Abrir com rasterio (suporta GeoTIFF com floating point)
                        with rasterio.open(img_path) as src:
                            # Ler primeira banda
                            band = src.read(1)
                            
                            # Normalizar valores float para 0-255 com melhor contraste
                            if band.dtype == np.float32 or band.dtype == np.float64:
                                # Remover NaN e valores inválidos
                                valid_mask = ~np.isnan(band)
                                if np.any(valid_mask):
                                    valid_data = band[valid_mask]
                                    band_min = np.percentile(valid_data, 2)  # 2° percentil para melhor contraste
                                    band_max = np.percentile(valid_data, 98)  # 98° percentil
                                    
                                    if band_max > band_min:
                                        band_norm = ((band - band_min) / (band_max - band_min) * 255).astype(np.uint8)
                                    else:
                                        band_norm = np.zeros_like(band, dtype=np.uint8)
                                else:
                                    band_norm = np.zeros_like(band, dtype=np.uint8)
                            else:
                                band_norm = band.astype(np.uint8)
                            
                            # APLICAR OVERLAY DE CRESCIMENTO
                            if mapa_crescimento is not None:
                                # Redimensionar mapa de crescimento para match da imagem atual
                                mapa_resized = np.array(Image.fromarray(mapa_crescimento.astype(np.uint8)).resize(
                                    (band_norm.shape[1], band_norm.shape[0]), Image.Resampling.NEAREST
                                ))
                                # Aplicar overlay colorido
                                band_rgb = self._aplicar_overlay_crescimento(band_norm, mapa_resized)
                                img = Image.fromarray(band_rgb, mode='RGB')
                            else:
                                img = Image.fromarray(band_norm, mode='L')
                                # Se não tem overlay, converter para RGB para consistência
                                img = img.convert('RGB')
                            
                            # Aumentar contraste (apenas se for escala cinza)
                            if mapa_crescimento is None:
                                enhancer = ImageEnhance.Contrast(img)
                                img = enhancer.enhance(1.5)
                            
                            # Redimensionar para tamanho maior e melhor qualidade
                            img = img.resize((1800, 1350), Image.Resampling.LANCZOS)
                            
                            # Converter para PNG em memória com boa qualidade
                            buffer = BytesIO()
                            img.save(buffer, format='PNG', optimize=False)
                            buffer.seek(0)
                            
                            # Codificar em base64
                            img_b64 = base64.b64encode(buffer.getvalue()).decode()
                            imagens_base64.append({
                                'nome': img_path.name,
                                'data': f'data:image/png;base64,{img_b64}'
                            })
                            logger.debug(f"✅ Imagem {idx+1} processada e adicionada (tamanho: {len(img_b64)} bytes)")
                            
                    except Exception as e:
                        logger.warning(f"Erro ao processar com rasterio {img_path.name}: {e}")
                        continue
                        
            except ImportError:
                # Fallback para PIL se rasterio não estiver disponível
                from PIL import Image, ImageEnhance
                import numpy as np
                
                for img_path in imagens_tif[:24]:
                    try:
                        img = Image.open(img_path)
                        if img.mode == 'RGB' or img.mode == 'RGBA':
                            img_array = np.array(img)
                            img = Image.fromarray(np.mean(img_array[:,:,:3], axis=2).astype(np.uint8), mode='L')
                        
                        # Aumentar contraste
                        enhancer = ImageEnhance.Contrast(img)
                        img = enhancer.enhance(1.5)
                        
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
                        
                    except Exception as e:
                        logger.warning(f"Erro ao processar com PIL {img_path.name}: {e}")
        
        except ImportError:
            logger.warning("PIL não disponível, criando timelapse com placeholder")
            # Usar placeholder se PIL não estiver disponível
            imagens_base64 = [{'nome': img.name, 'data': 'placeholder'} for img in imagens_tif[:12]]
        
        if not imagens_base64:
            logger.error("Nenhuma imagem pode ser processada")
            return None
        
        # Dados JSON para o timelapse
        dados_json = json.dumps({
            'cidade': dados_cidade['nome'],
            'crescimento': dados_cidade['crescimento'],
            'intensidade_inicial': dados_cidade['intensidade_inicial'],
            'intensidade_final': dados_cidade['intensidade_final'],
            'anos': dados_cidade['anos'],
            'cor_crescimento': '#FF4444' if dados_cidade['crescimento'] >= 5 else '#FFD700'
        }, ensure_ascii=False)
        
        
        logger.info(f"Total de imagens coletadas para timelapse: {len(imagens_base64)}")
        
        imagens_json = json.dumps(imagens_base64, ensure_ascii=False)
        
        # Criar HTML do timelapse
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Timelapse - ''' + dados_cidade['nome'] + '''</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1a1a1a; }
        
        .container {
            display: flex;
            flex-direction: column;
            height: 100vh;
            background: #0a0a0a;
        }
        
        .viewer {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            background: #222;
            overflow: hidden;
        }
        
        .imagem-container {
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .imagem-container img {
            width: 95%;
            height: 95%;
            object-fit: contain;
            display: block;
            image-rendering: high-quality;
            filter: contrast(1.2);
        }
        
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(ellipse at center, rgba(255, 100, 100, 0.3) 0%, transparent 70%);
            pointer-events: none;
        }
        
        .info-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 20px;
            border-radius: 8px;
            z-index: 100;
            max-width: 300px;
        }
        
        .info-panel h2 { margin: 0 0 10px 0; color: #333; font-size: 16px; }
        .info-panel p { margin: 5px 0; color: #666; font-size: 13px; }
        
        .growth-label {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 8px;
            font-size: 12px;
        }
        
        .growth-label.crescimento { background-color: #FF4444; color: white; }
        .growth-label.estavel { background-color: #FFD700; color: #333; }
        
        .controls {
            background: #222;
            padding: 20px;
            border-top: 1px solid #444;
        }
        
        .control-group {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 15px;
        }
        
        button {
            background: #FF4444;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }
        
        button:hover { background: #FF6666; }
        button:disabled { background: #888; cursor: not-allowed; }
        
        input[type="range"] {
            flex: 1;
            height: 6px;
            border-radius: 3px;
            background: #444;
            outline: none;
            -webkit-appearance: none;
        }
        
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #FF4444;
            cursor: pointer;
        }
        
        input[type="range"]::-moz-range-thumb {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #FF4444;
            cursor: pointer;
            border: none;
        }
        
        .tempo-display {
            color: #fff;
            font-size: 14px;
            min-width: 100px;
            text-align: center;
        }
        
        .legenda {
            color: #aaa;
            font-size: 12px;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #444;
        }
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
        const dados = ''' + dados_json + ''';
        const imagens = ''' + imagens_json + ''';
        
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
        
        function mostrarFrame(indice) {
            if (indice < 0 || indice >= imagens.length) return;
            
            indiceAtual = indice;
            const imagem = imagens[indice];
            
            if (imagem.data !== 'placeholder') {
                imgPrincipal.src = imagem.data;
            } else {
                imgPrincipal.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><rect width="800" height="600" fill="%23333"/><text x="400" y="300" fill="%23fff" text-anchor="middle" font-size="24">Imagem não disponível</text></svg>';
            }
            
            sliderTempo.value = indice;
            frameAtual.textContent = indice + 1;
        }
        
        function play() {
            if (tocando) return;
            tocando = true;
            btnPlay.disabled = true;
            btnPause.disabled = false;
            
            intervalo = setInterval(() => {
                if (indiceAtual < imagens.length - 1) {
                    mostrarFrame(indiceAtual + 1);
                } else {
                    clearInterval(intervalo);
                    tocando = false;
                    btnPlay.disabled = false;
                    btnPause.disabled = true;
                }
            }, 500);
        }
        
        function pausa() {
            tocando = false;
            btnPlay.disabled = false;
            btnPause.disabled = true;
            if (intervalo) clearInterval(intervalo);
        }
        
        btnPlay.addEventListener('click', play);
        btnPause.addEventListener('click', pausa);
        sliderTempo.addEventListener('input', (e) => {
            pausa();
            mostrarFrame(parseInt(e.target.value));
        });
        
        // Carregar primeiro frame
        mostrarFrame(0);
    </script>
</body>
</html>'''
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✅ Timelapse gerado para {nome_cidade}: {arquivo_saida}")
        return str(arquivo_saida)
    
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
        Calcula mapa de crescimento comparando duas imagens
        
        Returns:
            ndarray: Mapa com valores 0-2 (0=nada, 1=amarelo, 2=vermelho)
        """
        try:
            import numpy as np
            from PIL import Image
            
            # Garantir que as imagens têm o mesmo tamanho
            if imagem_inicio.shape != imagem_fim.shape:
                logger.warning(f"Imagens com tamanhos diferentes: {imagem_inicio.shape} vs {imagem_fim.shape}")
                logger.warning(f"Redimensionando segunda imagem para {imagem_inicio.shape}")
                
                # Redimensionar a segunda imagem para o tamanho da primeira
                img_fim_pil = Image.fromarray(imagem_fim.astype(np.uint8) if imagem_fim.max() > 1 else (imagem_fim * 255).astype(np.uint8))
                img_fim_pil = img_fim_pil.resize((imagem_inicio.shape[1], imagem_inicio.shape[0]), Image.Resampling.BILINEAR)
                imagem_fim = np.array(img_fim_pil).astype(imagem_fim.dtype)
            
            # Calcular diferença
            diferenca = imagem_fim - imagem_inicio
            
            # Inicializar mapa
            mapa = np.zeros_like(diferenca, dtype=np.uint8)
            
            # Filtrar apenas crescimento positivo significativo
            diff_crescimento = diferenca[~np.isnan(diferenca) & ~np.isinf(diferenca) & (diferenca > 0)]
            
            if len(diff_crescimento) > 0:
                # Calcular threshold mínimo
                p50 = np.percentile(diff_crescimento, 50)
                p75 = np.percentile(diff_crescimento, 75)
                p90 = np.percentile(diff_crescimento, 90)
                
                # Se não há variação (todos os valores são iguais), usar um threshold simples
                if (p90 - p50) < 0.01:  # Variação muito pequena
                    # Todos têm crescimento, então marcar como amarelo
                    mask_amarelo = diferenca >= p50
                    mapa[mask_amarelo] = 1
                else:
                    # Amarelo: crescimento moderado (p50 até p75)
                    mask_amarelo = (diferenca > p50) & (diferenca <= p75)
                    mapa[mask_amarelo] = 1
                    
                    # Vermelho: crescimento forte (acima de p75)
                    mask_vermelho = diferenca > p75
                    mapa[mask_vermelho] = 2
                
                logger.debug(f"Crescimento detectado: p50={p50:.2f}, p75={p75:.2f}, p90={p90:.2f}")
                logger.debug(f"Pixels amarelos: {np.sum(mapa == 1)}, Pixels vermelhos: {np.sum(mapa == 2)}")
            
            return mapa
            
        except Exception as e:
            logger.error(f"Erro ao calcular mapa de crescimento: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def _aplicar_overlay_crescimento(self, imagem_cinza, mapa_crescimento):
        """
        Aplica overlay de cores (amarelo/vermelho) em uma imagem
        
        Args:
            imagem_cinza: Imagem em escala de cinza (0-255)
            mapa_crescimento: Mapa de crescimento (0-2)
            
        Returns:
            Imagem RGB com overlay aplicado
        """
        try:
            import numpy as np
            from PIL import Image
            from scipy.ndimage import gaussian_filter
            
            # Criar imagem RGB duplicando o canal cinza
            altura, largura = imagem_cinza.shape
            imagem_rgb = np.stack([imagem_cinza] * 3, axis=2).astype(np.float32)
            
            if mapa_crescimento is not None:
                # Suavizar o mapa de crescimento para evitar artefatos
                mapa_suave = gaussian_filter(mapa_crescimento.astype(np.float32), sigma=1.5)
                
                # Vermelho: FF4444 (aplicar com transparência baseada na intensidade)
                mask_vermelho = mapa_suave > 1.5
                intensidade_vermelho = np.clip(mapa_suave[mask_vermelho] - 1.5, 0, 0.5) * 2
                
                imagem_rgb[mask_vermelho, 0] = np.clip(
                    imagem_rgb[mask_vermelho, 0] * (1 - intensidade_vermelho) + 255 * intensidade_vermelho, 
                    0, 255
                )
                imagem_rgb[mask_vermelho, 1] = np.clip(
                    imagem_rgb[mask_vermelho, 1] * (1 - intensidade_vermelho) + 68 * intensidade_vermelho, 
                    0, 255
                )
                imagem_rgb[mask_vermelho, 2] = np.clip(
                    imagem_rgb[mask_vermelho, 2] * (1 - intensidade_vermelho) + 68 * intensidade_vermelho, 
                    0, 255
                )
                
                # Amarelo: FFD700 (aplicar com transparência baseada na intensidade)
                mask_amarelo = (mapa_suave > 0.5) & (mapa_suave <= 1.5)
                intensidade_amarelo = np.clip(mapa_suave[mask_amarelo], 0.5, 1.5) / 1.5 * 0.6
                
                imagem_rgb[mask_amarelo, 0] = np.clip(
                    imagem_rgb[mask_amarelo, 0] * (1 - intensidade_amarelo) + 255 * intensidade_amarelo, 
                    0, 255
                )
                imagem_rgb[mask_amarelo, 1] = np.clip(
                    imagem_rgb[mask_amarelo, 1] * (1 - intensidade_amarelo) + 215 * intensidade_amarelo, 
                    0, 255
                )
                imagem_rgb[mask_amarelo, 2] = np.clip(
                    imagem_rgb[mask_amarelo, 2] * (1 - intensidade_amarelo) + 0 * intensidade_amarelo, 
                    0, 255
                )
            
            return imagem_rgb.astype(np.uint8)
            
        except Exception as e:
            logger.error(f"Erro ao aplicar overlay: {e}")
            return imagem_cinza
    
        """
        Gera pontos de heatmap distribuídos pela cidade baseado em intensidade
        
        Returns:
            list: Pontos no formato [[lat, lon, intensidade], ...]
        """
        try:
            pontos = []
            lat_centro = dados_cidade['lat']
            lon_centro = dados_cidade['lon']
            
            # Ler e processar dados do CSV
            import random
            random.seed(42)  # Para reproducibilidade
            
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
                return []
            
            anos = sorted(dados_por_ano.keys())
            ano_inicio = anos[0]
            ano_final = anos[-1]
            
            # Média por período
            media_inicio = sum(dados_por_ano[ano_inicio]) / len(dados_por_ano[ano_inicio])
            media_final = sum(dados_por_ano[ano_final]) / len(dados_por_ano[ano_final])
            
            # Calcular crescimento e gerar pontos
            crescimento = (media_final - media_inicio) / media_inicio if media_inicio > 0 else 0
            crescimento_norm = max(0, min(100, (crescimento + 1) * 50))  # Normalizar 0-100
            
            # Gerar pontos distribuídos pela cidade
            # Pontos com maior intensidade nas áreas com crescimento
            num_pontos = max(20, int(len(dados_por_ano[ano_final]) / 2))
            
            for i in range(num_pontos):
                # Distribuir pontos aleatoriamente dentro da bounding box da cidade
                lat_offset = (random.random() - 0.5) * 0.06
                lon_offset = (random.random() - 0.5) * 0.06
                
                # Intensidade varia com o crescimento
                if crescimento > 0:
                    # Com crescimento: pontos mais vermelhos
                    intensidade_ponto = 50 + (crescimento_norm * 0.5)
                else:
                    # Sem crescimento: pontos mais amarelos
                    intensidade_ponto = 40 + abs(crescimento_norm * 0.3)
                
                pontos.append([
                    lat_centro + lat_offset,
                    lon_centro + lon_offset,
                    intensidade_ponto
                ])
            
            logger.info(f"✅ {len(pontos)} pontos de heatmap gerados")
            return pontos
            
        except Exception as e:
            logger.error(f"Erro ao gerar heatmap: {e}")
            return []


def gerar_mapa_crescimento():
    """Função principal para gerar mapa"""
    print("🗺️ Gerando Mapa de Crescimento Luminoso...\n")
    
    mapa = MapaCrescimento()
    
    # Carregar coordenadas
    if not mapa.carregar_coordenadas():
        print("❌ Erro ao carregar coordenadas")
        return False
    
    # Processar crescimento
    print("\n📊 Calculando crescimento das cidades...")
    mapa.processar_todas_cidades()
    
    # Gerar outputs
    print("\n💾 Gerando arquivos...")
    mapa.gerar_geojson('mapa_crescimento.geojson')
    mapa.gerar_relatorio_html('mapa_crescimento.html')
    
    print("\n✅ Mapa gerado com sucesso!")
    print("\n📁 Arquivos gerados:")
    print("   • mapa_crescimento.html (Mapa interativo com todas as cidades)")
    print("   • mapa_crescimento.geojson (Dados GeoJSON com crescimento)")
    
    return True


if __name__ == "__main__":
    try:
        sucesso = gerar_mapa_crescimento()
        if sucesso:
            print("\n" + "="*60)
            print("🎉 Análise de Mapa de Crescimento Concluída!")
            print("="*60)
        else:
            print("\n⚠️  Falha ao gerar o mapa")
            exit(1)
    except KeyboardInterrupt:
        print("\n❌ Processo cancelado pelo usuário")
        exit(0)
    except Exception as e:
        logger.error(f"Erro ao executar: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


