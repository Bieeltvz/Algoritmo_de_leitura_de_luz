#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Heatmap de Crescimento Luminoso
Visualiza crescimento de luz por período com cores:
- Vermelho: crescimento luminoso
- Azul: diminuição luminosa
- Amarelo: estável
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from pathlib import Path
import csv
from collections import defaultdict
from typing import Dict, Tuple, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HeatmapCrescimento:
    """Gerador de heatmap de crescimento luminoso"""
    
    def __init__(self):
        """Inicializa o gerador"""
        self.dados_por_ano = defaultdict(lambda: defaultdict(list))
        self.anos_disponiveis = []
        
    def ler_csv(self, arquivo_csv: str) -> bool:
        """
        Lê arquivo CSV de resultados
        
        Args:
            arquivo_csv: Caminho do arquivo CSV
            
        Returns:
            bool: Sucesso na leitura
        """
        try:
            caminho = Path(arquivo_csv)
            if not caminho.exists():
                logger.error(f"Arquivo não encontrado: {arquivo_csv}")
                return False
            
            with open(arquivo_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ano = int(row['ano'])
                    mes = int(row['mes'])
                    intensidade = float(row['intensidade_media'])
                    
                    self.dados_por_ano[ano][mes] = intensidade
            
            self.anos_disponiveis = sorted(list(self.dados_por_ano.keys()))
            logger.info(f"✅ Lidos dados de {len(self.anos_disponiveis)} anos ({self.anos_disponiveis[0]}-{self.anos_disponiveis[-1]})")
            
            return len(self.anos_disponiveis) > 0
            
        except Exception as e:
            logger.error(f"Erro ao ler CSV: {e}")
            return False
    
    def calcular_crescimento(self) -> np.ndarray:
        """
        Calcula taxa de crescimento entre anos consecutivos
        
        Returns:
            np.ndarray: Matriz de crescimento (anos x meses)
                       -1 <= valor <= 1, onde:
                       > 0 = crescimento (vermelho)
                       < 0 = diminuição (azul)
                       ~0 = estável (amarelo)
        """
        if len(self.anos_disponiveis) < 2:
            logger.error("Precisa de pelo menos 2 anos de dados")
            return None
        
        # Inicializar matriz
        num_anos = len(self.anos_disponiveis) - 1  # Comparações entre anos
        matriz_crescimento = np.zeros((num_anos, 12))
        
        # Calcular crescimento para cada mês em comparação ao ano anterior
        for idx in range(len(self.anos_disponiveis) - 1):
            ano_anterior = self.anos_disponiveis[idx]
            ano_atual = self.anos_disponiveis[idx + 1]
            
            for mes in range(1, 13):
                # Obter intensidades
                int_anterior = self.dados_por_ano[ano_anterior].get(mes)
                int_atual = self.dados_por_ano[ano_atual].get(mes)
                
                if int_anterior is not None and int_atual is not None and int_anterior > 0:
                    # Calcular crescimento normalizado
                    crescimento = (int_atual - int_anterior) / int_anterior
                    
                    # Normalizar para intervalo [-1, 1]
                    crescimento_norm = np.clip(crescimento, -1, 1)
                    matriz_crescimento[idx, mes - 1] = crescimento_norm
                else:
                    # Dados faltando
                    matriz_crescimento[idx, mes - 1] = np.nan
        
        return matriz_crescimento
    
    def calcular_media_anual(self) -> np.ndarray:
        """
        Calcula intensidade média por mês em cada ano
        
        Returns:
            np.ndarray: Matriz de intensidades (anos x meses)
        """
        num_anos = len(self.anos_disponiveis)
        matriz_intensidade = np.zeros((num_anos, 12))
        
        for idx, ano in enumerate(self.anos_disponiveis):
            for mes in range(1, 13):
                intensidade = self.dados_por_ano[ano].get(mes, np.nan)
                matriz_intensidade[idx, mes - 1] = intensidade
        
        return matriz_intensidade
    
    def gerar_heatmap_crescimento(self, arquivo_saida: str = None) -> str:
        """
        Gera heatmap de crescimento luminoso
        
        Args:
            arquivo_saida: Caminho para salvar a imagem (opcional)
            
        Returns:
            str: Caminho do arquivo salvo
        """
        # Calcular crescimento
        matriz = self.calcular_crescimento()
        if matriz is None:
            return None
        
        # Criar colormap customizado: Azul (diminuição) -> Amarelo (estável) -> Vermelho (crescimento)
        cores = ['#0066CC', '#FFFF00', '#FF0000']  # Azul, Amarelo, Vermelho
        n_bins = 256
        cmap = LinearSegmentedColormap.from_list('crescimento', cores, N=n_bins)
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(14, 8), dpi=100)
        
        # Plot heatmap
        anos_labels = [f"{self.anos_disponiveis[i]}-{self.anos_disponiveis[i+1]}" 
                       for i in range(len(self.anos_disponiveis)-1)]
        meses_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        sns.heatmap(matriz, 
                   cmap=cmap,
                   cbar_kws={'label': 'Taxa de Crescimento (%)'},
                   xticklabels=meses_labels,
                   yticklabels=anos_labels,
                   ax=ax,
                   vmin=-1,
                   vmax=1,
                   center=0,
                   linewidths=0.5,
                   linecolor='white',
                   annot=True,
                   fmt='.2f',
                   annot_kws={'size': 8})
        
        # Formatar colorbar
        cbar = ax.collections[0].colorbar
        cbar.set_ticks([-1, -0.5, 0, 0.5, 1])
        cbar.set_ticklabels(['-100%', '-50%', '0%', '+50%', '+100%'])
        
        # Títulos e labels
        ax.set_title('Heatmap de Crescimento Luminoso Noturno\nAzul = Diminuição | Amarelo = Estável | Vermelho = Crescimento',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Mês', fontsize=12, fontweight='bold')
        ax.set_ylabel('Período (Ano1 → Ano2)', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        # Salvar
        if arquivo_saida is None:
            arquivo_saida = 'heatmap_crescimento.png'
        
        plt.savefig(arquivo_saida, dpi=100, bbox_inches='tight')
        logger.info(f"✅ Heatmap salvo: {arquivo_saida}")
        
        plt.close()
        return arquivo_saida
    
    def gerar_heatmap_intensidade(self, arquivo_saida: str = None) -> str:
        """
        Gera heatmap de intensidade luminosa por mês e ano
        
        Args:
            arquivo_saida: Caminho para salvar a imagem (opcional)
            
        Returns:
            str: Caminho do arquivo salvo
        """
        # Calcular média anual
        matriz = self.calcular_media_anual()
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(14, 8), dpi=100)
        
        # Plot heatmap com colormap viridis (padrão)
        anos_labels = [str(ano) for ano in self.anos_disponiveis]
        meses_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        sns.heatmap(matriz, 
                   cmap='YlOrRd',  # Yellow-Orange-Red para intensidade
                   cbar_kws={'label': 'Intensidade de Luz'},
                   xticklabels=meses_labels,
                   yticklabels=anos_labels,
                   ax=ax,
                   linewidths=0.5,
                   linecolor='white',
                   annot=True,
                   fmt='.1f',
                   annot_kws={'size': 8})
        
        # Títulos
        ax.set_title('Intensidade de Luz Noturna por Mês e Ano\nCores mais claras = Menor luz | Cores mais escuras = Maior luz',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Mês', fontsize=12, fontweight='bold')
        ax.set_ylabel('Ano', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        # Salvar
        if arquivo_saida is None:
            arquivo_saida = 'heatmap_intensidade.png'
        
        plt.savefig(arquivo_saida, dpi=100, bbox_inches='tight')
        logger.info(f"✅ Heatmap de intensidade salvo: {arquivo_saida}")
        
        plt.close()
        return arquivo_saida
    
    def gerar_heatmap_comparativo(self, arquivo_saida: str = None) -> str:
        """
        Gera heatmap comparativo com ambas as visualizações
        
        Args:
            arquivo_saida: Caminho para salvar a imagem (opcional)
            
        Returns:
            str: Caminho do arquivo salvo
        """
        # Calcular dados
        matriz_crescimento = self.calcular_crescimento()
        matriz_intensidade = self.calcular_media_anual()
        
        # Criar figura com subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), dpi=100)
        
        # --- Subplot 1: Crescimento ---
        anos_labels_crescimento = [f"{self.anos_disponiveis[i]}-{self.anos_disponiveis[i+1]}" 
                                   for i in range(len(self.anos_disponiveis)-1)]
        meses_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        cores = ['#0066CC', '#FFFF00', '#FF0000']
        n_bins = 256
        cmap_crescimento = LinearSegmentedColormap.from_list('crescimento', cores, N=n_bins)
        
        sns.heatmap(matriz_crescimento, 
                   cmap=cmap_crescimento,
                   cbar_kws={'label': 'Crescimento (%)'},
                   xticklabels=meses_labels,
                   yticklabels=anos_labels_crescimento,
                   ax=ax1,
                   vmin=-1,
                   vmax=1,
                   center=0,
                   linewidths=0.5,
                   linecolor='white',
                   annot=True,
                   fmt='.2f',
                   annot_kws={'size': 7})
        
        ax1.set_title('Taxa de Crescimento Anual\nAzul = Diminuição | Amarelo = Estável | Vermelho = Crescimento',
                     fontsize=12, fontweight='bold')
        ax1.set_xlabel('Mês', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Período (Ano1 → Ano2)', fontsize=11, fontweight='bold')
        
        # --- Subplot 2: Intensidade ---
        anos_labels_intensidade = [str(ano) for ano in self.anos_disponiveis]
        
        sns.heatmap(matriz_intensidade, 
                   cmap='YlOrRd',
                   cbar_kws={'label': 'Intensidade'},
                   xticklabels=meses_labels,
                   yticklabels=anos_labels_intensidade,
                   ax=ax2,
                   linewidths=0.5,
                   linecolor='white',
                   annot=True,
                   fmt='.1f',
                   annot_kws={'size': 7})
        
        ax2.set_title('Intensidade de Luz por Mês\nCores mais escuras = Maior intensidade',
                     fontsize=12, fontweight='bold')
        ax2.set_xlabel('Mês', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Ano', fontsize=11, fontweight='bold')
        
        fig.suptitle('Análise de Crescimento Luminoso Noturno (2014-2024)', 
                    fontsize=14, fontweight='bold', y=1.00)
        
        plt.tight_layout()
        
        # Salvar
        if arquivo_saida is None:
            arquivo_saida = 'heatmap_comparativo.png'
        
        plt.savefig(arquivo_saida, dpi=100, bbox_inches='tight')
        logger.info(f"✅ Heatmap comparativo salvo: {arquivo_saida}")
        
        plt.close()
        return arquivo_saida
    
    def gerar_relatorio(self) -> str:
        """
        Gera relatório textual do crescimento
        
        Returns:
            str: Relatório formatado
        """
        if not self.anos_disponiveis or len(self.anos_disponiveis) < 2:
            return "Dados insuficientes para gerar relatório"
        
        matriz_crescimento = self.calcular_crescimento()
        
        # Calcular estatísticas
        crescimento_medio = np.nanmean(matriz_crescimento)
        crescimento_max = np.nanmax(matriz_crescimento)
        crescimento_min = np.nanmin(matriz_crescimento)
        
        # Contar períodos
        crescimento_positivo = np.nansum(matriz_crescimento > 0.05)
        decrescimo = np.nansum(matriz_crescimento < -0.05)
        estavel = np.nansum((matriz_crescimento >= -0.05) & (matriz_crescimento <= 0.05))
        
        relatorio = f"""
╔════════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE CRESCIMENTO LUMINOSO                   ║
╚════════════════════════════════════════════════════════════════╝

📊 PERÍODO DE ANÁLISE:
  • Início: {self.anos_disponiveis[0]}
  • Fim: {self.anos_disponiveis[-1]}
  • Total: {len(self.anos_disponiveis)} anos

📈 ESTATÍSTICAS DE CRESCIMENTO:
  • Crescimento médio: {crescimento_medio*100:+.2f}%
  • Máximo crescimento: {crescimento_max*100:+.2f}%
  • Máximo decréscimo: {crescimento_min*100:+.2f}%

📍 CLASSIFICAÇÃO DOS PERÍODOS:
  • Períodos com crescimento (>5%): {int(crescimento_positivo)}
  • Períodos com decréscimo (<-5%): {int(decrescimo)}
  • Períodos estáveis (±5%): {int(estavel)}

💡 INTERPRETAÇÃO:
"""
        if crescimento_positivo > decrescimo:
            relatorio += "  ✓ Tendência predominante: CRESCIMENTO de luz\n"
        elif decrescimo > crescimento_positivo:
            relatorio += "  ✗ Tendência predominante: DECRÉSCIMO de luz\n"
        else:
            relatorio += "  ➜ Tendência predominante: ESTÁVEL\n"
        
        relatorio += f"""
🎨 CORES DO HEATMAP:
  🔵 Azul escuro = Decréscimo significativo (< -50%)
  🔵 Azul claro = Decréscimo moderado (-5% a -50%)
  🟡 Amarelo = Estável (±5%)
  🔴 Vermelho claro = Crescimento moderado (+5% a +50%)
  🔴 Vermelho escuro = Crescimento significativo (> +50%)

📌 OBSERVAÇÕES:
  • Cada célula representa o crescimento de um período anual específico
  • Valores positivos (vermelho) indicam urbanização
  • Valores negativos (azul) podem indicar economia ou despovoamento
  • Valores nulos (em branco) indicam dados faltando naquele mês
"""
        
        return relatorio


def teste_heatmap():
    """Testa o gerador de heatmap"""
    print("🧪 Testando Gerador de Heatmap de Crescimento...")
    
    gerador = HeatmapCrescimento()
    
    # Tentar encontrar arquivo CSV
    csv_file = Path('resultados_padrao.csv')
    if not csv_file.exists():
        # Procurar arquivos resultados_*
        csv_files = list(Path('.').glob('resultados_*.csv'))
        if csv_files:
            csv_file = csv_files[0]
            print(f"✅ Arquivo encontrado: {csv_file}")
        else:
            print("❌ Nenhum arquivo CSV encontrado")
            return False
    
    # Ler dados
    if not gerador.ler_csv(str(csv_file)):
        print("❌ Erro ao ler CSV")
        return False
    
    # Gerar heatmaps
    print("\n📊 Gerando heatmaps...")
    gerador.gerar_heatmap_crescimento('heatmap_crescimento.png')
    gerador.gerar_heatmap_intensidade('heatmap_intensidade.png')
    gerador.gerar_heatmap_comparativo('heatmap_comparativo.png')
    
    # Exibir relatório
    print("\n" + gerador.gerar_relatorio())
    
    print("\n✅ Teste concluído!")
    return True


if __name__ == '__main__':
    teste_heatmap()
