"""
Algoritmo para leitura e análise de sequências de imagens de satélite
- Valida pixels nulos (erros do satélite)
- Detecta outliers (valores muito altos)
- Calcula estatísticas de intensidade de luz
"""

import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass
import warnings

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ValidacaoPixel:
    """Resultado da validação de um pixel"""
    valor: float
    valido: bool
    tipo_erro: str = None  # 'nulo', 'outlier', None
    
    def __str__(self):
        if self.valido:
            return f"Pixel válido: {self.valor}"
        return f"Pixel INVÁLIDO ({self.tipo_erro}): {self.valor}"


@dataclass
class EstatisticasImagem:
    """Estatísticas de uma imagem processada"""
    total_pixels: int
    pixels_validos: int
    pixels_nulos: int
    pixels_outliers: int
    pixels_nodata: int  # NoData legítimo (geoespacial)
    percentual_valido: float
    intensidade_media: float
    intensidade_mediana: float
    intensidade_minima: float
    intensidade_maxima: float
    desvio_padrao: float
    threshold_outlier: float
    threshold_crescimento_luz: float  # Referência para comparação de crescimento de luz (média + desvio_padrão)


class AnalisadorLuzSatelite:
    """Analisador de intensidade de luz em imagens de satélite"""
    
    TAMANHO_ESPERADO = (500, 500)
    VALOR_NODATA_GEOESPACIAL = -9999  # Padrão para dados geoespaciais
    LIMIAR_OUTLIER_FIXO = 250  # Threshold fixo para detecção de outliers (intensidade luminosa)
    
    def __init__(self, metodo_outlier: str = 'iqr', limiar_iqr: float = 3.0, 
                 limiar_zscore: float = 3.0, modo_geoespacial: bool = False):
        """
        Args:
            metodo_outlier: 'iqr' (Intervalo Interquartil) ou 'zscore'
            limiar_iqr: Multiplicador do IQR para detecção de outliers
            limiar_zscore: Desvio padrão limite para detecção de outliers
            modo_geoespacial: Se True, diferencia NoData (-9999) de erros reais
        """
        self.metodo_outlier = metodo_outlier
        self.limiar_iqr = limiar_iqr
        self.limiar_zscore = limiar_zscore
        self.modo_geoespacial = modo_geoespacial
        
    def validar_dimensoes(self, imagem: np.ndarray) -> bool:
        """Valida se a imagem tem dimensões corretas (500x500)"""
        if imagem.shape != self.TAMANHO_ESPERADO:
            logger.warning(
                f"Dimensão incorreta: {imagem.shape} "
                f"(esperado {self.TAMANHO_ESPERADO})"
            )
            return False
        return True
    
    def detectar_pixels_nulos(self, imagem: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detecta pixels nulos (valor 0 ou NaN) e NoData geoespacial
        Retorna (máscara_nula, máscara_nodata)
        """
        if self.modo_geoespacial:
            # Em modo geoespacial:
            # - NoData (-9999) é ignorado mas não é "erro"
            # - Erros reais são 0 e NaN
            mascara_nodata = imagem == self.VALOR_NODATA_GEOESPACIAL
            mascara_nula = ((imagem == 0) | np.isnan(imagem)) & ~mascara_nodata
        else:
            # Modo normal: trata -9999 como erro
            mascara_nodata = np.zeros_like(imagem, dtype=bool)
            mascara_nula = (imagem == 0) | np.isnan(imagem) | (imagem == self.VALOR_NODATA_GEOESPACIAL)
        
        return mascara_nula, mascara_nodata
    
    def calcular_threshold_outlier(self, imagem: np.ndarray, 
                                   mascara_nula: np.ndarray,
                                   mascara_nodata: np.ndarray = None) -> float:
        """
        Calcula o threshold para detecção de outliers
        
        Usa threshold FIXO de 250 para identificar pixels com intensidade
        luminosa anormalmente alta (possíveis anomalias ou erros do sensor).
        
        Args:
            imagem: Array da imagem de satélite
            mascara_nula: Máscara de pixels nulos
            mascara_nodata: Máscara de pixels NoData (geoespacial)
            
        Returns:
            float: Threshold de 250 (intensidade luminosa máxima esperada)
        """
        # Retornar threshold fixo baseado em intensidade luminosa
        logger.debug(f"Threshold de outlier fixo: {self.LIMIAR_OUTLIER_FIXO}")
        return float(self.LIMIAR_OUTLIER_FIXO)
    
    def _threshold_iqr(self, pixels: np.ndarray) -> float:
        """
        [LEGADO] Threshold usando Intervalo Interquartil
        
        Mantido para compatibilidade, mas não é mais utilizado.
        Use LIMIAR_OUTLIER_FIXO em vez disto.
        """
        Q1 = np.percentile(pixels, 25)
        Q3 = np.percentile(pixels, 75)
        IQR = Q3 - Q1
        threshold = Q3 + (self.limiar_iqr * IQR)
        logger.debug(f"[LEGADO] IQR: {IQR}, Q1: {Q1}, Q3: {Q3}, Threshold: {threshold}")
        return threshold
    
    def _threshold_zscore(self, pixels: np.ndarray) -> float:
        """
        [LEGADO] Threshold usando Z-score
        
        Mantido para compatibilidade, mas não é mais utilizado.
        Use LIMIAR_OUTLIER_FIXO em vez disto.
        """
        media = np.mean(pixels)
        desvio = np.std(pixels)
        threshold = media + (self.limiar_zscore * desvio)
        logger.debug(f"[LEGADO] Média: {media}, Desvio: {desvio}, Threshold: {threshold}")
        return threshold
    
    def calcular_threshold_crescimento_luz(self, pixels: np.ndarray) -> float:
        """
        Calcula o threshold de crescimento de luz (referência para comparações entre imagens)
        
        Usa a fórmula: média + (0.5 * desvio_padrão)
        
        Este valor serve como ponto de referência para:
        - Comparar crescimento de luz entre imagens em diferentes períodos
        - Definir um "piso" esperado de intensidade luminosa
        - Analisar mudanças na iluminação urbana ao longo do tempo
        
        Args:
            pixels: Array de pixels válidos
            
        Returns:
            float: Threshold de crescimento de luz
        """
        media = np.mean(pixels)
        desvio = np.std(pixels)
        threshold_crescimento = media + (0.5 * desvio)
        logger.debug(f"Threshold crescimento: {threshold_crescimento:.2f} (média: {media:.2f}, desvio: {desvio:.2f})")
        return threshold_crescimento
    
    def detectar_outliers(self, imagem: np.ndarray, 
                         threshold: float) -> np.ndarray:
        """
        Detecta pixels outliers (acima do threshold)
        Retorna máscara booleana onde True = pixel outlier
        """
        mascara_outlier = imagem > threshold
        return mascara_outlier
    
    def validar_pixels(self, imagem: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Valida todos os pixels da imagem
        Retorna máscara de pixels válidos e dicionário com métricas
        """
        # Detectar pixels nulos e nodata
        mascara_nula, mascara_nodata = self.detectar_pixels_nulos(imagem)
        
        # Calcular threshold de outliers (ignorando nulos e nodata)
        threshold = self.calcular_threshold_outlier(imagem, mascara_nula, mascara_nodata)
        
        # Detectar outliers (apenas fora de nulos e nodata)
        mascara_outlier = self.detectar_outliers(imagem, threshold)
        mascara_outlier = mascara_outlier & ~(mascara_nula | mascara_nodata)
        
        # Máscara de pixels válidos
        mascara_valida = ~(mascara_nula | mascara_outlier | mascara_nodata)
        
        # Compilar métricas
        metricas = {
            'mascara_nula': mascara_nula,
            'mascara_nodata': mascara_nodata,
            'mascara_outlier': mascara_outlier,
            'threshold_outlier': threshold,
            'pixels_nulos': np.sum(mascara_nula),
            'pixels_nodata': np.sum(mascara_nodata),
            'pixels_outliers': np.sum(mascara_outlier),
        }
        
        return mascara_valida, metricas
    
    def processar_imagem(self, imagem: np.ndarray) -> EstatisticasImagem:
        """
        Processa uma imagem de satélite e retorna estatísticas
        """
        # Validar dimensões
        if not self.validar_dimensoes(imagem):
            logger.error("Imagem com dimensões incorretas!")
            raise ValueError(f"Esperado {self.TAMANHO_ESPERADO}, obtido {imagem.shape}")
        
        # Validar pixels
        mascara_valida, metricas = self.validar_pixels(imagem)
        
        # Extrair pixels válidos
        pixels_validos = imagem[mascara_valida]
        
        # Calcular estatísticas
        total_pixels = imagem.size
        pixels_validos_count = np.sum(mascara_valida)
        pixels_nulos = metricas['pixels_nulos']
        pixels_outliers = metricas['pixels_outliers']
        
        if pixels_validos_count == 0:
            logger.warning("Nenhum pixel válido para cálculo de estatísticas!")
            return EstatisticasImagem(
                total_pixels=total_pixels,
                pixels_validos=0,
                pixels_nulos=pixels_nulos,
                pixels_outliers=pixels_outliers,
                pixels_nodata=metricas.get('pixels_nodata', 0),
                percentual_valido=0.0,
                intensidade_media=0.0,
                intensidade_mediana=0.0,
                intensidade_minima=0.0,
                intensidade_maxima=0.0,
                desvio_padrao=0.0,
                threshold_outlier=metricas['threshold_outlier'],
                threshold_crescimento_luz=0.0
            )
        
        # Calcular percentual válido excluindo NoData
        pixels_nodata = metricas.get('pixels_nodata', 0)
        total_com_dados = total_pixels - pixels_nodata
        percentual_valido = (100.0 * pixels_validos_count / total_com_dados) if total_com_dados > 0 else 0.0
        
        # Calcular threshold de crescimento de luz
        threshold_crescimento = self.calcular_threshold_crescimento_luz(pixels_validos)
        
        # ⭐ Dados em escala bruta (0-1) sem conversão
        media_dados = np.mean(pixels_validos)
        max_dados = np.max(pixels_validos)
        
        # Escala bruta para cálculos mais precisos e thresholds úteis
        media_exibicao = media_dados
        mediana_exibicao = np.median(pixels_validos)
        minima_exibicao = np.min(pixels_validos)
        maxima_exibicao = max_dados
        desvio_exibicao = np.std(pixels_validos)
        
        stats = EstatisticasImagem(
            total_pixels=total_pixels,
            pixels_validos=pixels_validos_count,
            pixels_nulos=pixels_nulos,
            pixels_outliers=pixels_outliers,
            pixels_nodata=pixels_nodata,
            percentual_valido=percentual_valido,
            intensidade_media=media_exibicao,
            intensidade_mediana=mediana_exibicao,
            intensidade_minima=minima_exibicao,
            intensidade_maxima=maxima_exibicao,
            desvio_padrao=desvio_exibicao,
            threshold_outlier=metricas['threshold_outlier'],
            threshold_crescimento_luz=threshold_crescimento
        )
        
        return stats
    
    def processar_sequencia(self, imagens: List[np.ndarray]) -> List[EstatisticasImagem]:
        """
        Processa uma sequência de imagens
        """
        resultados = []
        logger.info(f"Processando sequência de {len(imagens)} imagens...")
        
        for idx, imagem in enumerate(imagens):
            try:
                stats = self.processar_imagem(imagem)
                resultados.append(stats)
                logger.info(
                    f"Imagem {idx+1}: "
                    f"Pixels válidos: {stats.pixels_validos}/{stats.total_pixels} "
                    f"({stats.percentual_valido:.2f}%), "
                    f"Média: {stats.intensidade_media:.2f}"
                )
            except Exception as e:
                logger.error(f"Erro ao processar imagem {idx+1}: {e}")
        
        return resultados
    
    def gerar_relatorio(self, stats: EstatisticasImagem) -> str:
        """Gera relatório formatado das estatísticas"""
        
        # Calcular totais com dados (excluindo NoData) para porcentagens coerentes
        total_com_dados = stats.total_pixels - stats.pixels_nodata
        percentual_nulos = (100 * stats.pixels_nulos / total_com_dados) if total_com_dados > 0 else 0
        percentual_outliers = (100 * stats.pixels_outliers / total_com_dados) if total_com_dados > 0 else 0
        
        # Preparar linha de NoData se em modo geoespacial
        linha_nodata = ""
        if self.modo_geoespacial and stats.pixels_nodata > 0:
            linha_nodata = f"  • Pixels NoData (fora cobertura): {stats.pixels_nodata:>10,} ({100*stats.pixels_nodata/stats.total_pixels:>6.2f}%)\n"
            nota_percentual = "(excluindo NoData)"
        else:
            nota_percentual = ""
        
        relatorio = f"""
╔════════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE ANÁLISE DE INTENSIDADE DE LUZ          ║
╚════════════════════════════════════════════════════════════════╝

📊 RESUMO DE VALIDAÇÃO:
  • Total de pixels:        {stats.total_pixels:>10,}
  • Pixels válidos:         {stats.pixels_validos:>10,} ({stats.percentual_valido:>6.2f}%) {nota_percentual}
  • Pixels nulos (erro):    {stats.pixels_nulos:>10,} ({percentual_nulos:>6.2f}%)
  • Pixels outliers:        {stats.pixels_outliers:>10,} ({percentual_outliers:>6.2f}%)
{linha_nodata}
💡 ESTATÍSTICAS DE INTENSIDADE (apenas pixels válidos):
  • Média:                  {stats.intensidade_media:>10.2f}
  • Mediana:                {stats.intensidade_mediana:>10.2f}
  • Mínima:                 {stats.intensidade_minima:>10.2f}
  • Máxima:                 {stats.intensidade_maxima:>10.2f}
  • Desvio padrão:          {stats.desvio_padrao:>10.2f}
 
🚨 THRESHOLDS:
  • Limite de outlier:      {stats.threshold_outlier:>10.2f}
  • Crescimento de luz:     {stats.threshold_crescimento_luz:>10.2f} (referência p/ comparação)
  
📈 QUALIDADE DA IMAGEM:
  • Status geral: {"✓ ACEITA" if stats.percentual_valido >= 90 else "⚠ VERIFICAR" if stats.percentual_valido >= 70 else "✗ REJEITADA"}
"""
        return relatorio
    
    def comparar_crescimento_luz(self, stats_anterior: EstatisticasImagem, 
                                 stats_atual: EstatisticasImagem) -> Dict:
        """
        Compara o crescimento de luz entre duas imagens utilizando thresholds para análise precisa.
        
        Estratégia de análise:
        1. Calcula a diferença de intensidade média
        2. Normaliza pela variância dos dados (desvio padrão)
        3. Compara contra os thresholds de crescimento estabelecidos
        4. Determina significância do crescimento baseado em critérios múltiplos
        
        Args:
            stats_anterior: Estatísticas da imagem anterior
            stats_atual: Estatísticas da imagem atual
            
        Returns:
            Dict com análise estruturada:
                - crescimento_media: Diferença bruta de intensidade
                - percentual_crescimento: % de mudança relativa
                - status_crescimento: CRESCIMENTO/DECRÉSCIMO/ESTÁVEL
                - crescimento_significativo: bool (excede thresholds)
                - diferenca_thresholds: Diferença entre thresholds de crescimento
                - detalhes: Métricas adicionais para debug
        """
        
        # ====== VALIDAÇÕES BÁSICAS ======
        if stats_anterior.pixels_validos == 0 or stats_atual.pixels_validos == 0:
            logger.warning("Uma ou ambas as imagens não possuem pixels válidos!")
            return {
                'crescimento_media': 0.0,
                'percentual_crescimento': 0.0,
                'status_crescimento': 'ERRO_DADOS_INSUFICIENTES',
                'crescimento_significativo': False,
                'diferenca_thresholds': 0.0,
                'detalhes': 'Imagem sem pixels válidos para comparação'
            }
        
        # ====== EXTRAIR VALORES PRINCIPAIS ======
        media_ant = stats_anterior.intensidade_media
        media_atu = stats_atual.intensidade_media
        desvio_ant = stats_anterior.desvio_padrao
        desvio_atu = stats_atual.desvio_padrao
        threshold_ant = stats_anterior.threshold_crescimento_luz
        threshold_atu = stats_atual.threshold_crescimento_luz
        
        # ====== CALCULAR CRESCIMENTO ======
        crescimento_media = media_atu - media_ant
        
        # Percentual de crescimento (normalizado)
        if media_ant > 0:
            percentual_crescimento = (crescimento_media / media_ant) * 100
        else:
            percentual_crescimento = 0.0
        
        # ====== CALCULAR NORMALIZAÇÃO POR VARIÂNCIA ======
        # Combina os desvios padrão para criar um fator de normalização
        desvio_medio = (desvio_ant + desvio_atu) / 2.0
        
        # Crescimento normalizado (quantos desvios padrão de mudança)
        if desvio_medio > 0:
            crescimento_normalizado = crescimento_media / desvio_medio
        else:
            crescimento_normalizado = 0.0
        
        # ====== ANÁLISE DE THRESHOLDS ======
        diferenca_thresholds = threshold_atu - threshold_ant
        
        # Crescimento relativo ao threshold
        crescimento_rel_threshold = (crescimento_media / threshold_ant * 100) if threshold_ant > 0 else 0
        
        # ====== DETERMINAR SIGNIFICÂNCIA ======
        # Critérios para considerar crescimento significativo:
        # 1. Crescimento absoluto > 10% do threshold anterior
        # 2. OU crescimento normalizado > 0.5 desvios padrão
        # 3. OU percentual crescimento > 5%
        
        limiar_abs = threshold_ant * 0.10  # 10% do threshold
        limiar_normalizado = 0.5  # Desvios padrão
        limiar_percentual = 5.0  # 5%
        
        crescimento_significativo = (
            (abs(crescimento_media) > limiar_abs) or
            (abs(crescimento_normalizado) > limiar_normalizado) or
            (abs(percentual_crescimento) > limiar_percentual)
        )
        
        # ====== CLASSIFICAR STATUS ======
        if abs(crescimento_media) < 0.5:
            status = 'ESTÁVEL'
        elif crescimento_media > 0:
            status = 'CRESCIMENTO'
        else:
            status = 'DECRÉSCIMO'
        
        # ====== CALCULAR QUALIDADE DA ANÁLISE ======
        # Verificar se ambas as imagens têm qualidade suficiente
        qualidade_min_aceitavel = 70.0
        qualidade_analise = (
            'CONFIÁVEL' if (stats_anterior.percentual_valido >= qualidade_min_aceitavel and 
                           stats_atual.percentual_valido >= qualidade_min_aceitavel)
            else 'BAIXA_QUALIDADE'
        )
        
        # ====== COMPILAR RESULTADO ======
        resultado = {
            'crescimento_media': float(crescimento_media),
            'percentual_crescimento': float(percentual_crescimento),
            'status_crescimento': status,
            'crescimento_significativo': crescimento_significativo,
            'diferenca_thresholds': float(diferenca_thresholds),
            'detalhes': {
                'media_anterior': float(media_ant),
                'media_atual': float(media_atu),
                'desvio_anterior': float(desvio_ant),
                'desvio_atual': float(desvio_atu),
                'crescimento_normalizado': float(crescimento_normalizado),
                'crescimento_rel_threshold': float(crescimento_rel_threshold),
                'qualidade_analise': qualidade_analise,
                'pixels_validos_anterior': stats_anterior.pixels_validos,
                'pixels_validos_atual': stats_atual.pixels_validos,
                'percentual_valido_anterior': float(stats_anterior.percentual_valido),
                'percentual_valido_atual': float(stats_atual.percentual_valido),
                'threshold_anterior': float(threshold_ant),
                'threshold_atual': float(threshold_atu),
            }
        }
        
        logger.info(
            f"Comparação realizada: {status} | "
            f"Crescimento: {crescimento_media:+.2f} ({percentual_crescimento:+.2f}%) | "
            f"Significativo: {crescimento_significativo} | "
            f"Qualidade: {qualidade_analise}"
        )
        
        return resultado


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def exemplo_uso():
    """Demonstra como usar o analisador"""
    
    # Criar analisador com método IQR
    analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0)
    
    # Simular 3 imagens de satélite (500x500)
    print("Gerando imagens de teste...")
    imagens_teste = []
    
    for i in range(3):
        # Gerar imagem com distribuição realista
        imagem = np.random.normal(loc=100, scale=20, size=(500, 500))
        imagem = np.clip(imagem, 0, 255).astype(np.uint8)
        
        # Adicionar alguns pixels nulos (erros do satélite)
        mascara_nula = np.random.random((500, 500)) < 0.02  # 2% nulos
        imagem[mascara_nula] = 0
        
        # Adicionar alguns outliers (valores muito altos)
        mascara_outlier = np.random.random((500, 500)) < 0.01  # 1% outliers
        imagem[mascara_outlier] = np.random.randint(230, 256, np.sum(mascara_outlier))
        
        imagens_teste.append(imagem.astype(float))
    
    # Processar sequência
    resultados = analisador.processar_sequencia(imagens_teste)
    
    # Exibir relatórios
    for idx, stats in enumerate(resultados):
        print(f"\n{'='*64}")
        print(f"IMAGEM {idx + 1}")
        print(analisador.gerar_relatorio(stats))


if __name__ == "__main__":
    exemplo_uso()
