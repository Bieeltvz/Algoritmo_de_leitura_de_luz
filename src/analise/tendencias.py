#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═════════════════════════════════════════════════════════════════════════════╗
║          📊 ANÁLISE DE TENDÊNCIAS - VISUALIZAR 10 ANOS DE DADOS             ║
║                         SEM DEPENDÊNCIAS EXTERNAS                           ║
╚═════════════════════════════════════════════════════════════════════════════╝

Analisa tendências de luz noturna dos dados processados.

Uso:
    python tendencias.py                              # Lê resultados.csv padrão
    python tendencias.py "Bombinhas_resultados.csv"  # Lê arquivo específico

Saída:
    - Relatório em texto (console)
    - tendencia_10anos.png: Gráfico da tendência
    - comparacao_primeiro_ultimo.png: Gráfico comparativo (2015 vs 2024)

Análises:
    - Tendência anual (média, min, max)
    - Crescimento percentual
    - Meses extremos (mais e menos brilhante)
    - Comparação primeiro vs último ano
"""

import sys
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnalisadorTendencias:
    """Analisa tendências de luz noturna"""
    
    def __init__(self):
        """Inicializa analisador"""
        self.dados = []
        self.por_ano = defaultdict(list)
        self.por_ano_mes = {}
    
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
            
            logger.info(f"✓ {len(self.dados)} registros carregados de {arquivo.name}")
            
            # Organizar por ano
            for registro in self.dados:
                ano = int(registro['ano'])
                mes = int(registro['mes'])
                intensidade = float(registro['intensidade_media'])
                
                self.por_ano[ano].append(intensidade)
                self.por_ano_mes[(ano, mes)] = intensidade
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao ler CSV: {e}")
            return False
    
    def calcular_tendencias(self):
        """Calcula tendências por ano"""
        tendencias = {}
        
        for ano in sorted(self.por_ano.keys()):
            intensidades = self.por_ano[ano]
            
            tendencias[ano] = {
                'media': sum(intensidades) / len(intensidades),
                'minimo': min(intensidades),
                'maximo': max(intensidades),
                'desvio': self._calcular_desvio(intensidades),
                'registros': len(intensidades),
            }
        
        return tendencias
    
    def _calcular_desvio(self, valores):
        """Calcula desvio padrão"""
        if not valores:
            return 0.0
        media = sum(valores) / len(valores)
        variancia = sum((x - media) ** 2 for x in valores) / len(valores)
        desvio = variancia ** 0.5
        return desvio
    
    def gerar_relatorio(self, arquivo_csv=None):
        """Gera relatório de tendências"""
        if arquivo_csv:
            if not self.ler_csv(arquivo_csv):
                return ""
        elif not self.dados:
            return "❌ Nenhum dado carregado"
        
        if not self.dados:
            return "❌ Arquivo CSV vazio"
        
        tendencias = self.calcular_tendencias()
        
        relatorio = []
        relatorio.append("\n" + "=" * 80)
        relatorio.append("📊 RELATÓRIO COMPLETO DE TENDÊNCIAS")
        relatorio.append("=" * 80)
        
        # Resumo geral
        relatorio.append(f"\n📁 Total de registros: {len(self.dados)}")
        
        if self.dados:
            percentuais = [float(r['percentual_valido']) for r in self.dados]
            qualidade_media = sum(percentuais) / len(percentuais)
            relatorio.append(f"✅ Qualidade média dos dados: {qualidade_media:.1f}%")
        
        # Tendência anual
        relatorio.append("\n" + "-" * 80)
        relatorio.append("📈 TENDÊNCIA ANUAL:")
        relatorio.append("-" * 80 + "\n")
        
        anos_lista = sorted(tendencias.keys())
        
        for ano in anos_lista:
            stats = tendencias[ano]
            relatorio.append(f"{ano}:")
            relatorio.append(f"  • Média:    {stats['media']:>8.2f}")
            relatorio.append(f"  • Mínimo:   {stats['minimo']:>8.2f}")
            relatorio.append(f"  • Máximo:   {stats['maximo']:>8.2f}")
            relatorio.append(f"  • Desvio:   {stats['desvio']:>8.2f}")
            relatorio.append(f"  • Registros: {stats['registros']} meses\n")
        
        # Extremos
        relatorio.append("-" * 80)
        relatorio.append("🌟 EXTREMOS:")
        relatorio.append("-" * 80 + "\n")
        
        # Mês mais brilhante
        max_mes = max(
            self.por_ano_mes.items(),
            key=lambda x: x[1]
        )
        relatorio.append(f"✨ Mês mais brilhante:")
        relatorio.append(f"   {max_mes[0][0]}/{max_mes[0][1]:02d}: {max_mes[1]:.2f}\n")
        
        # Mês menos brilhante
        min_mes = min(
            self.por_ano_mes.items(),
            key=lambda x: x[1]
        )
        relatorio.append(f"🌑 Mês menos brilhante:")
        relatorio.append(f"   {min_mes[0][0]}/{min_mes[0][1]:02d}: {min_mes[1]:.2f}\n")
        
        # Comparação primeiro vs último ano
        if len(anos_lista) > 1:
            relatorio.append("-" * 80)
            relatorio.append("🔄 COMPARAÇÃO PRIMEIRO vs ÚLTIMO ANO:")
            relatorio.append("-" * 80 + "\n")
            
            ano_inicio = anos_lista[0]
            ano_fim = anos_lista[-1]
            
            media_inicio = tendencias[ano_inicio]['media']
            media_fim = tendencias[ano_fim]['media']
            
            crescimento_absoluto = media_fim - media_inicio
            crescimento_percentual = (crescimento_absoluto / media_inicio * 100) if media_inicio != 0 else 0
            
            relatorio.append(f"  Ano inicial ({ano_inicio}):   {media_inicio:>8.2f}")
            relatorio.append(f"  Ano final ({ano_fim}):     {media_fim:>8.2f}")
            relatorio.append(f"  Crescimento:         +{crescimento_absoluto:>7.2f}")
            relatorio.append(f"  Percentual:          {crescimento_percentual:>+7.1f}%")
            
            meses_total = sum(
                tendencias[ano]['registros'] 
                for ano in [ano_inicio, ano_fim]
            )
            relatorio.append(f"  Dados coletados:     {meses_total} meses")
        
        # Gráficos
        relatorio.append("\n" + "-" * 80)
        relatorio.append("📊 GERANDO GRÁFICOS...")
        relatorio.append("-" * 80)
        
        try:
            self._gerar_graficos(tendencias)
            relatorio.append("\n✓ Gráficos gerados com sucesso!")
        except ImportError:
            relatorio.append("\n⚠️  matplotlib não disponível para gráficos")
        except Exception as e:
            relatorio.append(f"\n⚠️  Erro ao gerar gráficos: {e}")
        
        relatorio.append("\n" + "=" * 80 + "\n")
        
        return "\n".join(relatorio)
    
    def _gerar_graficos(self, tendencias):
        """Gera gráficos (requer matplotlib)"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
        except ImportError:
            logger.warning("matplotlib não instalado. Pulando gráficos.")
            return
        
        anos = sorted(tendencias.keys())
        medias = [tendencias[ano]['media'] for ano in anos]
        minimos = [tendencias[ano]['minimo'] for ano in anos]
        maximos = [tendencias[ano]['maximo'] for ano in anos]
        
        # Gráfico 1: Tendência 10 anos
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(anos, medias, 'b-o', linewidth=2, label='Média Anual')
        ax.fill_between(anos, minimos, maximos, alpha=0.2, color='blue', label='Min-Max')
        ax.set_xlabel('Ano', fontsize=12)
        ax.set_ylabel('Intensidade de Luz', fontsize=12)
        ax.set_title('📈 Tendência de Luz Noturna (10 Anos)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('tendencia_10anos.png', dpi=100)
        plt.close()
        logger.info("✓ Gráfico salvo: tendencia_10anos.png")
        
        # Gráfico 2: Comparação primeiro vs último
        if len(anos) > 1:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ano_inicio = anos[0]
            ano_fim = anos[-1]
            
            labels = [str(ano_inicio), str(ano_fim)]
            valores = [medias[0], medias[-1]]
            cores = ['#FF6B6B', '#4ECDC4']
            
            barras = ax.bar(labels, valores, color=cores, alpha=0.7, edgecolor='black', linewidth=2)
            
            # Adicionar valores nas barras
            for i, barra in enumerate(barras):
                altura = barra.get_height()
                ax.text(
                    barra.get_x() + barra.get_width()/2,
                    altura,
                    f'{valores[i]:.2f}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold'
                )
            
            # Percentual de crescimento
            crescimento = ((medias[-1] - medias[0]) / medias[0] * 100)
            ax.text(
                0.5, max(valores) * 0.9,
                f'Crescimento: {crescimento:+.1f}%',
                ha='center', fontsize=14, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5)
            )
            
            ax.set_ylabel('Intensidade de Luz', fontsize=12)
            ax.set_title('📊 Comparação: Primeiro vs Último Ano', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.tight_layout()
            plt.savefig('comparacao_primeiro_ultimo.png', dpi=100)
            plt.close()
            logger.info("✓ Gráfico salvo: comparacao_primeiro_ultimo.png")


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = 'resultados.csv'
    
    analisador = AnalisadorTendencias()
    relatorio = analisador.gerar_relatorio(arquivo)
    print(relatorio)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Análise cancelada")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro geral: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
