#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de PDF usando FPDF2 - Mtodo simples e confivel
Converte Markdown para PDF profissional com formatao
"""

from fpdf import FPDF
from pathlib import Path
import re

class PDFGerador(FPDF):
    """Classe customizada de PDF com cabealho e rodap"""
    
    def header(self):
        """Cabealho do documento"""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, '  Sistema de Anlise de Luz Noturna', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """Rodap com nmero de pgina"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pgina {self.page_no()}', 0, 0, 'C')

def ler_markdown(arquivo):
    """L arquivo Markdown"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        return f.read()

def processar_markdown(texto):
    """Processa texto Markdown em formato adequado para PDF"""
    linhas = texto.split('\n')
    blocos = []
    bloco_atual = {'tipo': 'texto', 'conteudo': []}
    
    i = 0
    while i < len(linhas):
        linha = linhas[i]
        
        # Headers
        if linha.startswith('# '):
            if bloco_atual['conteudo']:
                blocos.append(bloco_atual)
            blocos.append({'tipo': 'h1', 'conteudo': linha[2:].strip()})
            bloco_atual = {'tipo': 'texto', 'conteudo': []}
        elif linha.startswith('## '):
            if bloco_atual['conteudo']:
                blocos.append(bloco_atual)
            blocos.append({'tipo': 'h2', 'conteudo': linha[3:].strip()})
            bloco_atual = {'tipo': 'texto', 'conteudo': []}
        elif linha.startswith('### '):
            if bloco_atual['conteudo']:
                blocos.append(bloco_atual)
            blocos.append({'tipo': 'h3', 'conteudo': linha[4:].strip()})
            bloco_atual = {'tipo': 'texto', 'conteudo': []}
        # Cdigo
        elif linha.startswith('```'):
            if bloco_atual['conteudo']:
                blocos.append(bloco_atual)
                bloco_atual = {'tipo': 'texto', 'conteudo': []}
            
            codigo_linhas = []
            i += 1
            while i < len(linhas) and not linhas[i].startswith('```'):
                codigo_linhas.append(linhas[i])
                i += 1
            
            blocos.append({'tipo': 'codigo', 'conteudo': '\n'.join(codigo_linhas)})
        # Listas
        elif linha.startswith('- ') or linha.startswith('* '):
            if bloco_atual['conteudo'] and bloco_atual['tipo'] != 'lista':
                blocos.append(bloco_atual)
                bloco_atual = {'tipo': 'lista', 'conteudo': []}
            elif bloco_atual['tipo'] != 'lista':
                if bloco_atual['conteudo']:
                    blocos.append(bloco_atual)
                bloco_atual = {'tipo': 'lista', 'conteudo': []}
            
            bloco_atual['conteudo'].append(linha[2:].strip())
        # Linha vazia
        elif not linha.strip():
            if bloco_atual['conteudo']:
                blocos.append(bloco_atual)
                bloco_atual = {'tipo': 'texto', 'conteudo': []}
        # Texto normal
        else:
            if bloco_atual['tipo'] != 'texto':
                if bloco_atual['conteudo']:
                    blocos.append(bloco_atual)
                bloco_atual = {'tipo': 'texto', 'conteudo': []}
            bloco_atual['conteudo'].append(linha)
        
        i += 1
    
    if bloco_atual['conteudo']:
        blocos.append(bloco_atual)
    
    return blocos

def gerar_pdf(arquivo_md, arquivo_pdf):
    """Gera PDF a partir de Markdown"""
    
    print(f" Lendo arquivo: {arquivo_md}")
    texto = ler_markdown(arquivo_md)
    
    print(" Processando Markdown...")
    blocos = processar_markdown(texto)
    
    print(" Criando PDF...")
    pdf = PDFGerador()
    pdf.add_page()
    
    # Configurar fontes
    pdf.set_font('Arial', '', 11)
    
    for bloco in blocos:
        tipo = bloco['tipo']
        conteudo = bloco['conteudo']
        
        if tipo == 'h1':
            pdf.set_font('Arial', 'B', 18)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 12, conteudo, 0, 1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.ln(3)
        
        elif tipo == 'h2':
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(52, 73, 94)
            pdf.cell(0, 10, conteudo, 0, 1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.ln(2)
        
        elif tipo == 'h3':
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 9, conteudo, 0, 1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.ln(1)
        
        elif tipo == 'texto':
            pdf.set_font('Arial', '', 11)
            for linha in conteudo:
                if linha.strip():
                    # Substituir formatao Markdown simples
                    linha_proc = linha.replace('**', '*').replace('*', '')
                    pdf.multi_cell(0, 5, linha_proc)
                    pdf.ln(1)
        
        elif tipo == 'lista':
            pdf.set_font('Arial', '', 10)
            for item in conteudo:
                # Remover formatao
                item_limpo = item.replace('**', '').replace('*', '')
                pdf.cell(5, 6, '')
                print(f"Adding cell: {item_limpo}"); pdf.multi_cell(180, 6, item_limpo, border=0)
            pdf.ln(2)
        
        elif tipo == 'codigo':
            pdf.set_font('Courier', '', 9)
            pdf.set_fill_color(44, 62, 80)
            pdf.set_text_color(220, 220, 220)
            
            # Dividir cdigo em linhas
            linhas_codigo = conteudo.split('\n')
            for linha_cod in linhas_codigo[:50]:  # Limitar a 50 linhas
                if linha_cod.strip():
                    pdf.cell(0, 4, linha_cod[:95], 0, 1, fill=True)  # Limitar largura
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.ln(2)
        
        # Adicionar nova pgina se necessrio
        if pdf.will_page_break(10):
            pdf.add_page()
    
    print(f" Salvando: {arquivo_pdf}")
    pdf.output(arquivo_pdf)
    
    tamanho_mb = Path(arquivo_pdf).stat().st_size / (1024 * 1024)
    print(f" PDF gerado com sucesso!")
    print(f" Tamanho: {tamanho_mb:.2f} MB")
    
    return True

if __name__ == '__main__':
    print("=" * 70)
    print("  GERADOR DE PDF - DOCUMENTAO DO SISTEMA DE LUZ NOTURNA")
    print("=" * 70)
    print()
    
    arquivo_md = Path('DOCUMENTACAO_COMPLETA_CLEAN.md')
    arquivo_pdf = Path('DOCUMENTACAO_COMPLETA.pdf')
    
    if not arquivo_md.exists():
        print(f" Arquivo no encontrado: {arquivo_md}")
    else:
        try:
            gerar_pdf(str(arquivo_md), str(arquivo_pdf))
            print()
            print("=" * 70)
            print(" Documentao pronta!")
            print("=" * 70)
        except Exception as e:
            print(f" Erro: {e}")
            import traceback
            traceback.print_exc()

