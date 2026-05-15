#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═════════════════════════════════════════════════════════════════════════════╗
║              🤖 AUTOMAÇÃO - PROCESSAMENTO INCREMENTAL DIÁRIO                ║
║               Processa APENAS imagens novas (modificadas)                   ║
║                      SEM REPROCESSAMENTO                                    ║
╚═════════════════════════════════════════════════════════════════════════════╝

Monitora pasta e processa automaticamente imagens novas.

Uso:
    python automacao.py                     # Executa uma vez
    python automacao.py --schedule "02:00"  # Agenda para 2 AM diariamente

Saída:
    - Append a resultados.csv com imagens novas
    - automacao.log: Log de execuções
    - last_run.txt: Data/hora da última execução

Vantagens:
    - Processa APENAS arquivos novos (não reprocessa)
    - Append automático ao CSV
    - Sem reprocessamento
    - Totalmente automático
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
import os
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automacao.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Automacao:
    """Automação de processamento incremental"""
    
    ARQUIVO_ULTIMA_EXECUCAO = Path('last_run.txt')
    ARQUIVO_CACHE = Path('processados.json')
    ARQUIVO_RESULTADOS = Path('resultados.csv')
    PASTA_MONITORADA = Path(r"C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Bombinhas_recorte")
    
    def __init__(self):
        """Inicializa automação"""
        self.ultima_execucao = self._carregar_ultima_execucao()
        logger.info("🤖 Automação inicializada")
    
    def _carregar_ultima_execucao(self):
        """Carrega timestamp da última execução"""
        if self.ARQUIVO_ULTIMA_EXECUCAO.exists():
            try:
                with open(self.ARQUIVO_ULTIMA_EXECUCAO, 'r') as f:
                    timestamp = float(f.read().strip())
                    logger.info(f"Última execução: {datetime.fromtimestamp(timestamp)}")
                    return timestamp
            except Exception as e:
                logger.warning(f"Erro ao carregar última execução: {e}")
        return 0.0
    
    def _salvar_ultima_execucao(self):
        """Salva timestamp da execução atual"""
        try:
            with open(self.ARQUIVO_ULTIMA_EXECUCAO, 'w') as f:
                f.write(str(time.time()))
        except Exception as e:
            logger.error(f"Erro ao salvar última execução: {e}")
    
    def buscar_novas_imagens(self):
        """
        Encontra imagens modificadas desde última execução
        
        Returns:
            list: Caminhos das imagens novas/modificadas
        """
        novas_imagens = []
        
        if not self.PASTA_MONITORADA.exists():
            logger.error(f"Pasta não encontrada: {self.PASTA_MONITORADA}")
            return novas_imagens
        
        for arquivo in self.PASTA_MONITORADA.rglob('*.tif*'):
            tempo_modificacao = os.path.getmtime(arquivo)
            
            if tempo_modificacao > self.ultima_execucao:
                novas_imagens.append(arquivo)
                logger.info(f"✓ Nova imagem encontrada: {arquivo.name}")
        
        return novas_imagens
    
    def processar_incrementais(self):
        """Processa apenas imagens novas"""
        logger.info("🔍 Buscando imagens novas...")
        
        novas_imagens = self.buscar_novas_imagens()
        
        if not novas_imagens:
            logger.info("✓ Nenhuma imagem nova encontrada")
            return
        
        logger.info(f"📊 {len(novas_imagens)} imagens novas encontradas")
        
        # Importar processador
        from processador_paralelo import ProcessadorParalelo
        
        processador = ProcessadorParalelo()
        
        # Processar em paralelo (mas apenas os novos)
        print("\n" + "=" * 80)
        print("🚀 PROCESSAMENTO INCREMENTAL AUTOMÁTICO")
        print("=" * 80)
        print(f"📊 Imagens novas: {len(novas_imagens)}")
        print("-" * 80)
        
        for imagem in novas_imagens:
            resultado = processador.processar_arquivo(imagem)
            if resultado:
                print(f"✓ Processado: {resultado['arquivo']}")
                # Append ao CSV
                self._append_csv(resultado)
        
        # Salvar cache atualizado
        processador._salvar_cache()
        
        print("-" * 80)
        print(f"✅ Processamento concluído!")
        print(f"📄 Resultados appended a: {self.ARQUIVO_RESULTADOS}")
        print("=" * 80 + "\n")
    
    def _append_csv(self, resultado):
        """Append um resultado ao CSV"""
        try:
            modo_escrita = 'a' if self.ARQUIVO_RESULTADOS.exists() else 'w'
            escrever_header = not self.ARQUIVO_RESULTADOS.exists()
            
            import csv
            with open(self.ARQUIVO_RESULTADOS, modo_escrita, newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=resultado.keys())
                if escrever_header:
                    writer.writeheader()
                writer.writerow(resultado)
        except Exception as e:
            logger.error(f"Erro ao append CSV: {e}")
    
    def agendar(self, hora="02:00"):
        """
        Agenda execução automática
        
        Args:
            hora: Hora da execução (formato "HH:MM")
        """
        try:
            import schedule
        except ImportError:
            logger.error("Pacote 'schedule' não instalado!")
            logger.info("Instale com: pip install schedule")
            return
        
        logger.info(f"📅 Agendando execução para {hora} todos os dias...")
        
        horas, minutos = map(int, hora.split(':'))
        
        def tarefa():
            logger.info("⏰ Iniciando processamento automático agendado...")
            self.ultima_execucao = self._carregar_ultima_execucao()
            self.processar_incrementais()
            self._salvar_ultima_execucao()
            logger.info("✅ Processamento agendado concluído")
        
        schedule.every().day.at(f"{horas:02d}:{minutos:02d}").do(tarefa)
        
        logger.info("🤖 Agendador ativo. Pressione Ctrl+C para parar...")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("\n❌ Agendador parado pelo usuário")


def main():
    """Função principal"""
    automacao = Automacao()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--schedule":
            hora = sys.argv[2] if len(sys.argv) > 2 else "02:00"
            automacao.agendar(hora)
        else:
            logger.info(f"Argumento desconhecido: {sys.argv[1]}")
    else:
        # Executa uma vez
        logger.info("▶️  Executando processamento incremental uma vez...")
        automacao.processar_incrementais()
        automacao._salvar_ultima_execucao()
        logger.info("✅ Execução concluída")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n❌ Automação cancelada")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro geral: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
