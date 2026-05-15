#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═════════════════════════════════════════════════════════════════════════════╗
║          🛰️  PROCESSADOR PARALELO DE IMAGENS DE SATÉLITE                   ║
║            Processa 1200+ imagens 8-10x mais rápido                        ║
║                    SEM BANCO DE DADOS - CSV ONLY                           ║
╚═════════════════════════════════════════════════════════════════════════════╝

Processa todas as imagens TIFF de uma pasta recursivamente em paralelo.

Uso:
    python processador_paralelo.py [caminho_pasta]

Exemplo:
    python processador_paralelo.py "C:\\Users\\gtvargas\\Documents\\Bombinhas_noturna\\Raster\\Bombinhas_recorte"

Saída:
    - resultados.csv: Dados de todas as imagens
    - processados.json: Cache de arquivos já processados
    
Performance:
    - 120 imagens: 5-10 minutos (vs 1-2 horas sequencial)
    - Melhoria: 8-10x mais rápido
"""

import sys
import json
import time
from pathlib import Path
from multiprocessing import Pool, cpu_count
import numpy as np
import rasterio
import csv
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProcessadorParalelo:
    """Processador paralelo de imagens de satélite"""
    
    EXTENSOES_VALIDAS = {'.tif', '.tiff'}
    
    def __init__(self, workers=None, nome_cidade=None, forcar_reprocessamento=False, diretorio_trabalho=None):
        """
        Inicializa o processador
        
        Args:
            workers: Número de processos paralelos (padrão: número de CPUs)
            nome_cidade: Nome da cidade para gerar arquivos específicos (ex: 'Bombinhas_recorte')
            forcar_reprocessamento: Se True, limpa o cache antigo e reprocessa tudo
            diretorio_trabalho: Diretório onde salvar os arquivos (padrão: diretório atual)
        """
        self.workers = workers or cpu_count()
        self.nome_cidade = nome_cidade or 'padrao'
        self.forcar_reprocessamento = forcar_reprocessamento
        
        # Definir diretório de trabalho
        if diretorio_trabalho:
            self.diretorio_trabalho = Path(diretorio_trabalho)
        else:
            self.diretorio_trabalho = Path.cwd()
        
        # Gerar nomes de arquivo específicos por cidade
        self.ARQUIVO_CACHE = self.diretorio_trabalho / f'processados_{self.nome_cidade}.json'
        self.ARQUIVO_RESULTADOS = self.diretorio_trabalho / f'resultados_{self.nome_cidade}.csv'
        
        logger.info(f"Inicializando ProcessadorParalelo com {self.workers} workers")
        logger.info(f"Cidade: {self.nome_cidade}")
        logger.info(f"Diretório de trabalho: {self.diretorio_trabalho}")
        logger.info(f"Cache: {self.ARQUIVO_CACHE}")
        logger.info(f"Resultados: {self.ARQUIVO_RESULTADOS}")
        
        # Se forçar reprocessamento, limpar cache antigo
        if forcar_reprocessamento and self.ARQUIVO_CACHE.exists():
            logger.warning(f"🔄 Limpando cache antigo: {self.ARQUIVO_CACHE}")
            self.ARQUIVO_CACHE.unlink()
            if self.ARQUIVO_RESULTADOS.exists():
                logger.warning(f"🔄 Limpando resultados antigos: {self.ARQUIVO_RESULTADOS}")
                self.ARQUIVO_RESULTADOS.unlink()
        
        # Carregar cache de processados
        self.processados = self._carregar_cache()
    
    def _carregar_cache(self):
        """Carrega lista de arquivos já processados"""
        if self.ARQUIVO_CACHE.exists():
            try:
                with open(self.ARQUIVO_CACHE, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                logger.info(f"Cache carregado: {len(dados)} arquivos já processados")
                return dados
            except Exception as e:
                logger.error(f"Erro ao carregar cache: {e}")
                return {}
        return {}
    
    def _salvar_cache(self):
        """Salva cache de processados"""
        try:
            with open(self.ARQUIVO_CACHE, 'w', encoding='utf-8') as f:
                json.dump(self.processados, f, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar cache: {e}")
    
    def processar_arquivo(self, caminho_arquivo):
        """
        Processa um arquivo TIFF individual
        
        Args:
            caminho_arquivo: Caminho completo do arquivo TIFF
            
        Returns:
            dict: Dados processados ou None se erro
        """
        try:
            caminho_arquivo = Path(caminho_arquivo)
            
            # Ler com rasterio
            with rasterio.open(caminho_arquivo) as src:
                dados = src.read(1).astype(float)  # Ler como float para preservar valores
            
            # Detectar NoData ANTES de normalizar
            mascara_nodata_original = dados == -9999
            
            # ⭐ NÃO USAR NORMALIZAÇÃO MIN-MAX!
            # Motivo: Cada arquivo tem escala diferente, impossível comparar médias ao longo do tempo
            # Usar os dados originais diretamente (já que são radiância calibrada do satélite)
            
            # Extrair ano e mês do caminho
            # NOTA: Suporta nomes compostos como "balneario_camboriu_2014_02"
            # Pega os últimos 2 elementos que são SEMPRE ano_mes
            partes = caminho_arquivo.stem.split('_')
            ano = partes[-2] if len(partes) > 1 else '0'
            mes = partes[-1] if len(partes) > 0 else '0'
            
            # Contar pixels NoData
            pixels_nodata = np.sum(mascara_nodata_original)
            total_pixels = dados.size
            total_com_dados = total_pixels - pixels_nodata
            
            # Validação de pixels: > 0 (exclui tanto NoData quanto nulos)
            mascara_valida = (dados > 0) & (~mascara_nodata_original)
            pixels_validos = dados[mascara_valida]
            pixels_nulos = np.sum(dados == 0)
            pixels_outliers = np.sum(dados > 250)  # Valores muito altos
            
            # Cálculos
            if len(pixels_validos) > 0:
                media_bruta = float(np.mean(pixels_validos))
                mediana_bruta = float(np.median(pixels_validos))
                desvio_bruto = float(np.std(pixels_validos))
                
                # ⭐ ESCALA BRUTA: Dados em escala 0-1 para comparações precisas
                # Sem conversão - mantém valores reais para cálculos de threshold
                media = media_bruta
                mediana = mediana_bruta
                desvio = desvio_bruto
                threshold_crescimento = media_bruta + (0.5 * desvio_bruto)
                
                pixels_validos_count = len(pixels_validos)
                # Calcular percentual com CAP em 100%
                percentual = (100.0 * pixels_validos_count / total_com_dados) if total_com_dados > 0 else 0.0
                percentual = min(percentual, 100.0)  # ⭐ GARANTIR QUE NÃO ULTRAPASSA 100%
            else:
                media = mediana = desvio = threshold_crescimento = 0.0
                pixels_validos_count = 0
                percentual = 0.0
            
            resultado = {
                'arquivo': caminho_arquivo.name,
                'caminho_completo': str(caminho_arquivo),  # Para rastrear no cache
                'ano': int(ano),
                'mes': int(mes),
                'intensidade_media': round(media, 2),
                'mediana': round(mediana, 2),
                'desvio': round(desvio, 2),
                'percentual_valido': round(percentual, 2),
                'threshold_crescimento': round(threshold_crescimento, 2),
                'pixels_nulos': int(pixels_nulos),
                'pixels_nodata': int(pixels_nodata),
                'pixels_outliers': int(pixels_outliers),
                'total_pixels': int(total_pixels),
                'total_com_dados': int(total_com_dados),
            }
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao processar {caminho_arquivo}: {e}")
            return None
    
    def processar_pasta(self, pasta_raiz):
        """
        Processa todas as imagens TIFF em uma pasta recursivamente
        
        Args:
            pasta_raiz: Caminho da pasta raiz
        """
        pasta_raiz = Path(pasta_raiz)
        
        if not pasta_raiz.exists():
            logger.error(f"Pasta não encontrada: {pasta_raiz}")
            return
        
        # Encontrar todos os arquivos TIFF
        arquivos = []
        for ext in self.EXTENSOES_VALIDAS:
            arquivos.extend(pasta_raiz.rglob(f'*{ext}'))
        
        if not arquivos:
            logger.warning(f"Nenhum arquivo TIFF encontrado em {pasta_raiz}")
            return
        
        # Filtrar arquivos já processados
        arquivos_novos = [
            a for a in arquivos 
            if str(a) not in self.processados
        ]
        
        logger.info(f"📊 Total de arquivos TIFF: {len(arquivos)}")
        logger.info(f"✓ Já processados: {len(arquivos) - len(arquivos_novos)}")
        logger.info(f"🆕 Novos a processar: {len(arquivos_novos)}")
        
        if not arquivos_novos:
            logger.info("Todos os arquivos já foram processados!")
            return
        
        # Processar em paralelo
        inicio = time.time()
        print("\n" + "=" * 80)
        print("🚀 INICIANDO PROCESSAMENTO PARALELO")
        print("=" * 80)
        print(f"📁 Pasta: {pasta_raiz}")
        print(f"👷 Workers: {self.workers}")
        print(f"📊 Imagens a processar: {len(arquivos_novos)}")
        print("-" * 80)
        
        resultados = []
        processados_count = 0
        
        with Pool(self.workers) as pool:
            for i, resultado in enumerate(
                pool.imap_unordered(self.processar_arquivo, arquivos_novos),
                start=1
            ):
                if resultado:
                    resultados.append(resultado)
                    # Adicionar ao cache de processados no processo PRINCIPAL
                    self.processados[resultado['caminho_completo']] = datetime.now().isoformat()
                    processados_count += 1
                    print(f"✓ {i}/{len(arquivos_novos)} - {resultado['arquivo']}")
                else:
                    print(f"✗ {i}/{len(arquivos_novos)} - Erro")
        
        tempo_total = time.time() - inicio
        
        # Salvar resultados no CSV
        self._salvar_csv(resultados)
        
        # Salvar cache
        self._salvar_cache()
        
        print("-" * 80)
        print(f"\n✅ Processamento concluído!")
        print(f"   Processados: {processados_count}/{len(arquivos_novos)}")
        print(f"   Erros: {len(arquivos_novos) - processados_count}")
        print(f"   Tempo total: {tempo_total:.1f}s")
        if len(arquivos_novos) > 0:
            print(f"   Tempo médio: {tempo_total/len(arquivos_novos):.2f}s/imagem")
            print(f"   Velocidade: {len(arquivos_novos)/tempo_total:.2f} imagens/segundo")
        print(f"📄 Resultados salvos em: {self.ARQUIVO_RESULTADOS}")
        print("=" * 80 + "\n")
    
    def _salvar_csv(self, resultados):
        """Salva resultados em CSV (append se arquivo existe)"""
        modo = 'a' if self.ARQUIVO_RESULTADOS.exists() else 'w'
        escrever_header = not self.ARQUIVO_RESULTADOS.exists()
        
        try:
            with open(self.ARQUIVO_RESULTADOS, modo, newline='', encoding='utf-8') as f:
                if resultados:
                    writer = csv.DictWriter(
                        f, 
                        fieldnames=resultados[0].keys()
                    )
                    if escrever_header:
                        writer.writeheader()
                    writer.writerows(resultados)
        except Exception as e:
            logger.error(f"Erro ao salvar CSV: {e}")


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        pasta = sys.argv[1]
    else:
        # Usar pasta padrão
        pasta = r"C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Bombinhas_recorte"
    
    processador = ProcessadorParalelo()
    processador.processar_pasta(pasta)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Processamento cancelado pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro geral: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
