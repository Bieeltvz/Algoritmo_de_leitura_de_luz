#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter documentação Markdown em PDF
Usa reportlab para criar um PDF profissional com formatação
"""

from pathlib import Path
from markdown2pdf.converter import Converter
import sys

def gerar_pdf():
    """Gera PDF a partir do Markdown"""
    
    md_file = Path("DOCUMENTACAO_COMPLETA.md")
    pdf_file = Path("DOCUMENTACAO_COMPLETA.pdf")
    
    if not md_file.exists():
        print(f"❌ Arquivo não encontrado: {md_file}")
        return False
    
    try:
        print(f"📄 Lendo arquivo: {md_file}")
        
        # Converter usando markdown2pdf
        converter = Converter(str(md_file))
        
        print(f"🔄 Convertendo para PDF...")
        converter.convert()
        converter.write_pdf(str(pdf_file))
        
        # Verificar se foi criado
        if pdf_file.exists():
            tamanho_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"\n✅ PDF gerado com sucesso!")
            print(f"📁 Arquivo: {pdf_file}")
            print(f"📊 Tamanho: {tamanho_mb:.2f} MB")
            return True
        else:
            print(f"❌ Falha ao criar PDF")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")
        print(f"\n🔧 Tentando método alternativo com weasyprint...")
        
        try:
            from weasyprint import HTML
            HTML(string=converter_md_para_html(str(md_file))).write_pdf(str(pdf_file))
            print(f"✅ PDF gerado com weasyprint!")
            return True
        except Exception as e2:
            print(f"❌ Erro também no método alternativo: {e2}")
            return False

def converter_md_para_html(md_file):
    """Converte Markdown para HTML básico"""
    import markdown
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
            h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
            h2 {{ color: #555; margin-top: 30px; }}
            h3 {{ color: #666; }}
            code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
            pre {{ background-color: #f4f4f4; padding: 15px; border-left: 4px solid #007bff; }}
            table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
            table, th, td {{ border: 1px solid #ddd; }}
            th, td {{ padding: 12px; text-align: left; }}
            th {{ background-color: #007bff; color: white; }}
            ul, ol {{ line-height: 2; }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """

if __name__ == '__main__':
    print("=" * 70)
    print("🛰️  GERADOR DE DOCUMENTAÇÃO PDF")
    print("=" * 70)
    print()
    
    sucesso = gerar_pdf()
    
    if sucesso:
        print("\n✨ Documentação pronta para uso!")
        sys.exit(0)
    else:
        print("\n⚠️  Verifique os erros acima")
        sys.exit(1)
