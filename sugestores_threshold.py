#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sugestor de Thresholds para Análise de Crescimento de Luz Noturna
Analisa dados anuais e sugere valores ótimos de threshold para comparações

Usa estatísticas dos anos disponíveis para gerar recomendações inteligentes
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SugestorThreshold:
    """Sugere valores de threshold para análise de crescimento de luz"""
    
    def __init__(self):
        """Inicializa sugestor"""
        self.dados = []
        self.por_ano = defaultdict(list)
        self.por_ano_mes = {}
        self.stats_por_ano = {}
        
    def ler_csv(self, arquivo_csv):
        """
        Lê arquivo CSV de resultados
        
        Args:
            arquivo_csv: Caminho do arquivo CSV
            
        Returns:
            bool: True se leitura bem-sucedida
        """
        arquivo = Path(arquivo_csv)
        
        if not arquivo.exists():
            logger.error(f"Arquivo não encontrado: {arquivo}")
            return False
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.dados = list(reader)
            
            logger.info(f"✓ {len(self.dados)} registros carregados")
            
            # Organizar por ano
            for registro in self.dados:
                try:
                    ano = int(registro['ano'])
                    mes = int(registro['mes'])
                    intensidade = float(registro['intensidade_media'])
                    
                    self.por_ano[ano].append({
                        'mes': mes,
                        'intensidade': intensidade,
                        'registro': registro
                    })
                    self.por_ano_mes[(ano, mes)] = intensidade
                except (ValueError, KeyError):
                    continue
            
            return len(self.por_ano) > 0
            
        except Exception as e:
            logger.error(f"Erro ao ler CSV: {e}")
            return False
    
    def calcular_stats_anuais(self):
        """Calcula estatísticas para cada ano"""
        self.stats_por_ano = {}
        
        for ano in sorted(self.por_ano.keys()):
            dados_ano = self.por_ano[ano]
            intensidades = [d['intensidade'] for d in dados_ano]
            
            if not intensidades:
                continue
            
            # Calcular estatísticas
            media = sum(intensidades) / len(intensidades)
            minimo = min(intensidades)
            maximo = max(intensidades)
            
            # Desvio padrão
            variancia = sum((x - media) ** 2 for x in intensidades) / len(intensidades)
            desvio = variancia ** 0.5
            
            # Percentil 25 e 75
            sorted_intensidades = sorted(intensidades)
            p25 = sorted_intensidades[len(sorted_intensidades) // 4]
            p75 = sorted_intensidades[3 * len(sorted_intensidades) // 4]
            iqr = p75 - p25
            
            self.stats_por_ano[ano] = {
                'media': media,
                'minimo': minimo,
                'maximo': maximo,
                'desvio': desvio,
                'p25': p25,
                'p75': p75,
                'iqr': iqr,
                'registros': len(intensidades),
                'dados': dados_ano
            }
    
    def sugerir_thresholds(self) -> Dict:
        """
        Sugere valores de threshold baseado na análise dos dados anuais
        
        Returns:
            Dict com sugestões e recomendações
        """
        if not self.stats_por_ano:
            return {'erro': 'Sem dados para análise'}
        
        anos_disponiveis = sorted(self.stats_por_ano.keys())
        
        # Calcular crescimento geral
        primeiro_ano = anos_disponiveis[0]
        ultimo_ano = anos_disponiveis[-1]
        
        media_primeiro = self.stats_por_ano[primeiro_ano]['media']
        media_ultimo = self.stats_por_ano[ultimo_ano]['media']
        
        crescimento_absoluto = media_ultimo - media_primeiro
        crescimento_percentual = (crescimento_absoluto / media_primeiro * 100) if media_primeiro > 0 else 0
        
        # Análise por faixa de intensidade
        todas_intensidades = []
        for stats in self.stats_por_ano.values():
            todas_intensidades.extend([d['intensidade'] for d in stats['dados']])
        
        todas_intensidades.sort()
        media_geral = sum(todas_intensidades) / len(todas_intensidades)
        desvio_geral = (sum((x - media_geral) ** 2 for x in todas_intensidades) / len(todas_intensidades)) ** 0.5
        
        # Sugestões de threshold
        sugestoes = {
            'periodos': {
                'primeiro_ano': primeiro_ano,
                'ultimo_ano': ultimo_ano,
                'total_anos': len(anos_disponiveis),
                'anos_disponiveis': anos_disponiveis
            },
            'crescimento': {
                'absoluto': round(crescimento_absoluto, 2),
                'percentual': round(crescimento_percentual, 2),
                'tendencia': 'crescimento' if crescimento_percentual > 5 else ('estável' if crescimento_percentual > -5 else 'declínio')
            },
            'thresholds_sugeridos': {
                'conservador': round(media_geral - desvio_geral, 2),
                'moderado': round(media_geral, 2),
                'agressivo': round(media_geral + desvio_geral, 2),
                'alto_crescimento': round(media_geral + 2 * desvio_geral, 2)
            },
            'estatisticas_gerais': {
                'media_geral': round(media_geral, 2),
                'desvio_geral': round(desvio_geral, 2),
                'minimo_geral': round(min(todas_intensidades), 2),
                'maximo_geral': round(max(todas_intensidades), 2),
                'total_registros': len(todas_intensidades)
            },
            'comparacao_periodos': self._comparar_periodos(),
            'recomendacoes': self._gerar_recomendacoes(crescimento_percentual, media_primeiro, media_ultimo)
        }
        
        return sugestoes
    
    def _comparar_periodos(self) -> Dict:
        """Compara estatísticas entre início e fim do período"""
        anos_disponiveis = sorted(self.stats_por_ano.keys())
        
        if len(anos_disponiveis) < 2:
            return {}
        
        # Dividir em dois períodos
        meio = len(anos_disponiveis) // 2
        anos_inicio = anos_disponiveis[:meio]
        anos_fim = anos_disponiveis[meio:]
        
        # Calcular médias por período
        medias_inicio = []
        medias_fim = []
        
        for ano in anos_inicio:
            medias_inicio.append(self.stats_por_ano[ano]['media'])
        
        for ano in anos_fim:
            medias_fim.append(self.stats_por_ano[ano]['media'])
        
        media_periodo_inicio = sum(medias_inicio) / len(medias_inicio) if medias_inicio else 0
        media_periodo_fim = sum(medias_fim) / len(medias_fim) if medias_fim else 0
        
        crescimento_periodo = media_periodo_fim - media_periodo_inicio
        crescimento_percentual_periodo = (crescimento_periodo / media_periodo_inicio * 100) if media_periodo_inicio > 0 else 0
        
        return {
            'periodo_inicio': f"{min(anos_inicio)}-{max(anos_inicio)}",
            'periodo_fim': f"{min(anos_fim)}-{max(anos_fim)}",
            'media_inicio': round(media_periodo_inicio, 2),
            'media_fim': round(media_periodo_fim, 2),
            'crescimento_absoluto': round(crescimento_periodo, 2),
            'crescimento_percentual': round(crescimento_percentual_periodo, 2)
        }
    
    def _gerar_recomendacoes(self, crescimento_pct: float, media_inicio: float, media_fim: float) -> List[str]:
        """Gera recomendações baseadas no crescimento"""
        recomendacoes = []
        
        if crescimento_pct > 20:
            recomendacoes.append("⚠️ Crescimento FORTE de luz detectado (>20%). Use threshold AGRESSIVO para capturar mudanças.")
        elif crescimento_pct > 10:
            recomendacoes.append("📈 Crescimento significativo detectado (10-20%). Use threshold MODERADO a AGRESSIVO.")
        elif crescimento_pct > 0:
            recomendacoes.append("📊 Leve crescimento detectado. Use threshold MODERADO para análises comparativas.")
        elif crescimento_pct > -10:
            recomendacoes.append("📉 Leve declínio detectado. Use threshold CONSERVADOR para sentar mudanças.")
        else:
            recomendacoes.append("⚠️ Declínio significativo detectado (>10%). Investigar possíveis causas de redução de luz.")
        
        if media_fim > media_inicio * 1.5:
            recomendacoes.append("🔴 A intensidade de luz aumentou 50% ou mais! Possível urbanização acelerada.")
        
        recomendacoes.append("💡 Dica: Use o threshold MODERADO (média geral) para comparações entre anos diferentes.")
        
        return recomendacoes
    
    def encontrar_imagens_exemplo(self, numero_exemplos: int = 1) -> Dict:
        """
        Encontra imagens exemplares dos períodos inicial e final
        
        Args:
            numero_exemplos: Número de exemplos por período
            
        Returns:
            Dict com informações de imagens exemplo
        """
        anos_disponiveis = sorted(self.stats_por_ano.keys())
        
        if len(anos_disponiveis) < 2:
            return {}
        
        primeiro_ano = anos_disponiveis[0]
        ultimo_ano = anos_disponiveis[-1]
        
        exemplos_inicio = self._selecionar_melhores_imagens(primeiro_ano, numero_exemplos)
        exemplos_fim = self._selecionar_melhores_imagens(ultimo_ano, numero_exemplos)
        
        return {
            'periodo_inicio': {
                'ano': primeiro_ano,
                'imagens': exemplos_inicio
            },
            'periodo_fim': {
                'ano': ultimo_ano,
                'imagens': exemplos_fim
            }
        }
    
    def _selecionar_melhores_imagens(self, ano: int, numero: int = 1) -> List[Dict]:
        """Seleciona imagens variadas de um ano (máximo, mínimo, média e aleatórios)"""
        if ano not in self.stats_por_ano:
            return []
        
        dados_ano = self.stats_por_ano[ano]['dados']
        
        if not dados_ano:
            return []
        
        # Ordenar por intensidade
        dados_ordenados = sorted(dados_ano, key=lambda x: x['intensidade'], reverse=True)
        
        # Selecionar imagens variadas
        resultado = []
        indices_usados = set()
        
        # 1. Imagem com MAIOR intensidade (pico de luz)
        if dados_ordenados and 0 not in indices_usados:
            dado = dados_ordenados[0]
            arquivo = dado['registro'].get('arquivo', f"{ano}-{dado['mes']:02d}")
            resultado.append({
                'indice': len(resultado) + 1,
                'arquivo': arquivo,
                'mes': dado['mes'],
                'intensidade': round(dado['intensidade'], 2),
                'titulo': f"Máximo - {ano} (Mês {dado['mes']:02d})",
                'tipo': '📈 Pico de Luz'
            })
            indices_usados.add(0)
        
        # 2. Imagem com MENOR intensidade (mínimo de luz)
        if len(dados_ordenados) > 1 and (len(dados_ordenados) - 1) not in indices_usados:
            dado = dados_ordenados[-1]
            arquivo = dado['registro'].get('arquivo', f"{ano}-{dado['mes']:02d}")
            resultado.append({
                'indice': len(resultado) + 1,
                'arquivo': arquivo,
                'mes': dado['mes'],
                'intensidade': round(dado['intensidade'], 2),
                'titulo': f"Mínimo - {ano} (Mês {dado['mes']:02d})",
                'tipo': '📉 Menor Luz'
            })
            indices_usados.add(len(dados_ordenados) - 1)
        
        # 3. Imagem na MEDIANA (representativo)
        if len(dados_ordenados) > 2:
            indice_mediana = len(dados_ordenados) // 2
            if indice_mediana not in indices_usados:
                dado = dados_ordenados[indice_mediana]
                arquivo = dado['registro'].get('arquivo', f"{ano}-{dado['mes']:02d}")
                resultado.append({
                    'indice': len(resultado) + 1,
                    'arquivo': arquivo,
                    'mes': dado['mes'],
                    'intensidade': round(dado['intensidade'], 2),
                    'titulo': f"Mediano - {ano} (Mês {dado['mes']:02d})",
                    'tipo': '➡️ Típico'
                })
                indices_usados.add(indice_mediana)
        
        # Limitar ao número de exemplos solicitados
        return resultado[:numero]


def analisar_e_sugerir_thresholds(arquivo_csv: str) -> Dict:
    """
    Função principal para análise e sugestão de thresholds
    
    Args:
        arquivo_csv: Caminho do arquivo CSV com resultados
        
    Returns:
        Dict com análise completa e sugestões
    """
    sugestor = SugestorThreshold()
    
    if not sugestor.ler_csv(arquivo_csv):
        return {'erro': 'Não foi possível ler o arquivo CSV'}
    
    sugestor.calcular_stats_anuais()
    sugestoes = sugestor.sugerir_thresholds()
    exemplos = sugestor.encontrar_imagens_exemplo(numero_exemplos=3)  # 3 exemplos: máximo, mínimo, mediano
    
    sugestoes['exemplos_imagens'] = exemplos
    sugestoes['anos_com_dados'] = {
        ano: {
            'media': round(stats['media'], 2),
            'minimo': round(stats['minimo'], 2),
            'maximo': round(stats['maximo'], 2),
            'desvio': round(stats['desvio'], 2),
            'registros': stats['registros']
        }
        for ano, stats in sugestor.stats_por_ano.items()
    }
    
    return sugestoes


if __name__ == '__main__':
    # Exemplo de uso
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python sugestores_threshold.py <arquivo_csv>")
        sys.exit(1)
    
    resultado = analisar_e_sugerir_thresholds(sys.argv[1])
    
    import json
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
