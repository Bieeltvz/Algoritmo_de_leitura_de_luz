#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   🛰️  ANÁLISE DE LUZ NOTURNA - VERSÃO PARALELA              ║
║                         SEM BANCO DE DADOS - CSV ONLY                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Menu principal para processar 1200+ imagens de satélite em paralelo.

Uso:
    python main.py [opcao]

Opções:
    1 - Processar todas as imagens (primeira vez)
    2 - Ver tendências e gráficos
    3 - Configurar automação (Windows Task Scheduler)
    4 - Ver status de processamento
    5 - Limpar cache e começar do zero

Exemplo:
    python main.py 1           # Processar todas as imagens
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
import time

# Diretório do projeto
PROJECT_DIR = Path(__file__).parent


def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_titulo(titulo):
    """Exibe um título formatado"""
    print("=" * 80)
    print(f"  {titulo}")
    print("=" * 80)


def opcao_1_processar():
    """Processa todas as imagens em paralelo"""
    limpar_tela()
    print_titulo("🚀 PROCESSANDO TODAS AS IMAGENS")
    
    print("\n⚠️  ATENÇÃO: Esta operação pode levar 5-10 minutos")
    print("   Imagens: ~120")
    print("   Tempo estimado: 5-10 minutos")
    print("   Velocidade: 8-10x mais rápido que sequencial\n")
    
    confirmar = input("Deseja continuar? (S/N): ").strip().upper()
    if confirmar != 'S':
        print("❌ Operação cancelada")
        return
    
    print("\n⏳ Iniciando processamento...")
    print("-" * 80)
    
    try:
        from processador_paralelo import ProcessadorParalelo
        
        # Pasta base
        pasta_base = Path(r"C:\Users\gtvargas\Documents\Bombinhas_noturna\Raster\Bombinhas_recorte")
        
        if not pasta_base.exists():
            print(f"❌ Pasta não encontrada: {pasta_base}")
            print(f"\n💡 Dica: Verifique se o caminho está correto")
            return
        
        inicio = time.time()
        
        processador = ProcessadorParalelo()
        processador.processar_pasta(str(pasta_base))
        
        tempo_total = time.time() - inicio
        
        print("-" * 80)
        print(f"\n✅ Processamento concluído em {tempo_total:.1f} segundos!")
        print(f"📄 Resultados salvos em: resultados.csv")
        print(f"💾 Cache atualizado em: processados.json")
        
    except Exception as e:
        print(f"❌ Erro durante processamento: {e}")
        import traceback
        traceback.print_exc()


def opcao_2_tendencias():
    """Exibe tendências e gera gráficos"""
    limpar_tela()
    print_titulo("📊 ANALISANDO TENDÊNCIAS")
    
    print("\n⏳ Processando dados...")
    print("-" * 80)
    
    try:
        from tendencias import AnalisadorTendencias
        
        csv_arquivo = Path("resultados.csv")
        
        if not csv_arquivo.exists():
            print("❌ Arquivo resultados.csv não encontrado")
            print("\n💡 Dica: Execute primeiro a opção 1 (Processar todas as imagens)")
            return
        
        analisador = AnalisadorTendencias()
        relatorio = analisador.gerar_relatorio(str(csv_arquivo))
        
        print(relatorio)
        
        print("\n" + "-" * 80)
        print("✅ Gráficos gerados:")
        print("   📊 tendencia_10anos.png")
        print("   📊 comparacao_primeiro_ultimo.png")
        
    except Exception as e:
        print(f"❌ Erro ao gerar tendências: {e}")
        import traceback
        traceback.print_exc()


def opcao_3_automacao():
    """Configura automação no Windows Task Scheduler"""
    limpar_tela()
    print_titulo("🤖 CONFIGURAR AUTOMAÇÃO")
    
    print("\nA automação processa imagens novas automaticamente todos os dias às 2 AM.")
    print("\n" + "-" * 80)
    print("\n1️⃣  Primeiro, instale o pacote 'schedule':")
    print("    pip install schedule\n")
    
    input("Pressione ENTER depois de instalar...")
    
    print("\n2️⃣  Agora vou criar a tarefa automática...\n")
    
    # Path dos arquivos
    python_exe = sys.executable
    script_path = Path(__file__).parent / "automacao.py"
    script_path = script_path.resolve()
    
    # Comando para criar tarefa (Windows)
    if os.name == 'nt':
        cmd = (
            f'schtasks /create /tn "Analise_Luz_Diaria" '
            f'/tr "\\"{python_exe}\\" \\"{script_path}\\"" '
            f'/sc daily /st 02:00 /f'
        )
        
        print("Copie e execute este comando no PowerShell (como Administrador):\n")
        print("─" * 80)
        print(cmd)
        print("─" * 80)
        
        confirmar = input("\n✓ Você quer que eu execute este comando? (S/N): ").strip().upper()
        
        if confirmar == 'S':
            try:
                import subprocess
                print("\n⏳ Criando tarefa...")
                subprocess.run(cmd, shell=True, check=True)
                print("✅ Tarefa criada com sucesso!")
                print("\n📋 Informações:")
                print("   • Tarefa: Analise_Luz_Diaria")
                print("   • Horário: 02:00 (2 AM)")
                print("   • Frequência: Diária")
                print("   • Ação: Processa imagens novas automaticamente")
                print("\n📝 Para ver logs: automacao.log")
            except Exception as e:
                print(f"❌ Erro ao criar tarefa: {e}")
    else:
        print("ℹ️  Para Linux/Mac, use crontab:")
        print(f"\n   crontab -e")
        print(f"   # Adicionar esta linha:")
        print(f"   0 2 * * * cd {Path(__file__).parent} && {python_exe} automacao.py\n")


def opcao_4_status():
    """Exibe status de processamento"""
    limpar_tela()
    print_titulo("📊 STATUS DE PROCESSAMENTO")
    
    csv_arquivo = Path("resultados.csv")
    processados_arquivo = Path("processados.json")
    log_arquivo = Path("automacao.log")
    
    print("\n📁 Arquivos:")
    print(f"   {'resultados.csv':<30} {('✓ Existe' if csv_arquivo.exists() else '✗ Não existe')}")
    print(f"   {'processados.json':<30} {('✓ Existe' if processados_arquivo.exists() else '✗ Não existe')}")
    print(f"   {'automacao.log':<30} {('✓ Existe' if log_arquivo.exists() else '✗ Não existe')}")
    
    print("\n📊 Estatísticas:")
    
    if csv_arquivo.exists():
        with open(csv_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            print(f"   Registros em resultados.csv: {len(linhas) - 1}")
    else:
        print(f"   Registros em resultados.csv: 0")
    
    if processados_arquivo.exists():
        try:
            with open(processados_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                print(f"   Arquivos processados: {len(dados)}")
                print(f"   Última atualização: {datetime.fromtimestamp(os.path.getmtime(processados_arquivo)).strftime('%d/%m/%Y %H:%M')}")
        except:
            pass
    else:
        print(f"   Arquivos processados: 0")
    
    if log_arquivo.exists():
        print(f"   Última automação: {datetime.fromtimestamp(os.path.getmtime(log_arquivo)).strftime('%d/%m/%Y %H:%M')}")
    else:
        print(f"   Última automação: Nunca executada")
    
    print("\n" + "-" * 80)


def opcao_5_limpar():
    """Limpa cache e começa do zero"""
    limpar_tela()
    print_titulo("🔄 LIMPAR CACHE E COMEÇAR DO ZERO")
    
    print("\n⚠️  ATENÇÃO: Isto vai:")
    print("   • Excluir processados.json (cache)")
    print("   • Manter resultados.csv (dados)")
    print("   • Forçar reprocessamento de todas as imagens\n")
    
    confirmar = input("Deseja continuar? (S/N): ").strip().upper()
    if confirmar != 'S':
        print("❌ Operação cancelada")
        return
    
    processados_arquivo = Path("processados.json")
    if processados_arquivo.exists():
        processados_arquivo.unlink()
        print("✅ Cache limpo!")
        print("\n💡 Dica: Execute novamente a opção 1 para reprocessar")
    else:
        print("ℹ️  Cache já está vazio")


def menu_principal():
    """Exibe menu principal"""
    while True:
        limpar_tela()
        print_titulo("🛰️  ANÁLISE DE LUZ NOTURNA - MENU PRINCIPAL")
        
        print("\nOpções:")
        print("  1️⃣  Processar todas as imagens (5-10 min)")
        print("  2️⃣  Ver tendências e gráficos")
        print("  3️⃣  Configurar automação (Task Scheduler)")
        print("  4️⃣  Ver status de processamento")
        print("  5️⃣  Limpar cache e começar do zero")
        print("  0️⃣  Sair")
        
        print("\n" + "-" * 80)
        opcao = input("Escolha uma opção (0-5): ").strip()
        
        if opcao == "1":
            opcao_1_processar()
        elif opcao == "2":
            opcao_2_tendencias()
        elif opcao == "3":
            opcao_3_automacao()
        elif opcao == "4":
            opcao_4_status()
        elif opcao == "5":
            opcao_5_limpar()
        elif opcao == "0":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")
            time.sleep(1)
        
        input("\n\nPressione ENTER para continuar...")


def main():
    """Função principal"""
    
    # Se passou argumento, executa diretamente
    if len(sys.argv) > 1:
        opcao = sys.argv[1]
        
        if opcao == "1":
            opcao_1_processar()
        elif opcao == "2":
            opcao_2_tendencias()
        elif opcao == "3":
            opcao_3_automacao()
        elif opcao == "4":
            opcao_4_status()
        elif opcao == "5":
            opcao_5_limpar()
        else:
            print(f"❌ Opção {opcao} inválida")
            print(__doc__)
    else:
        # Modo interativo
        menu_principal()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
