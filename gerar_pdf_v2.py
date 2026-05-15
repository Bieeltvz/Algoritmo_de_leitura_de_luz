#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de PDF a partir de Markdown
Usa método de conversão puro sem dependências externas complexas
"""

from pathlib import Path
import subprocess
import sys

def gerar_pdf_com_pandoc():
    """Tenta usar pandoc se disponível (melhor qualidade)"""
    try:
        print("🔍 Procurando pandoc...")
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
        
        print("✅ Pandoc encontrado! Convertendo...")
        subprocess.run([
            'pandoc',
            'DOCUMENTACAO_COMPLETA.md',
            '-o', 'DOCUMENTACAO_COMPLETA.pdf',
            '--pdf-engine=wkhtmltopdf',
            '-V', 'geometry:margin=1in',
            '-V', 'fontsize=11pt'
        ], check=True)
        
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def gerar_pdf_com_weasyprint():
    """Usa weasyprint como alternativa"""
    try:
        from weasyprint import HTML
        import markdown
        
        print("📝 Lendo Markdown...")
        with open('DOCUMENTACAO_COMPLETA.md', 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        print("🔄 Convertendo Markdown para HTML...")
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'nl2br', 'sane_lists']
        )
        
        # Envolver em HTML com estilos
        html_final = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Documentação do Sistema de Análise de Luz Noturna</title>
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            padding: 40px;
            background-color: #fff;
        }}
        
        h1 {{
            font-size: 28px;
            color: #2c3e50;
            border-bottom: 4px solid #3498db;
            padding-bottom: 15px;
            margin: 30px 0 20px 0;
            page-break-after: avoid;
        }}
        
        h2 {{
            font-size: 22px;
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin: 25px 0 15px 0;
            page-break-after: avoid;
        }}
        
        h3 {{
            font-size: 16px;
            color: #555;
            margin: 15px 0 10px 0;
            page-break-after: avoid;
        }}
        
        p {{
            margin: 10px 0;
            text-align: justify;
        }}
        
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 10px;
        }}
        
        li {{
            margin: 8px 0;
            line-height: 1.6;
        }}
        
        code {{
            background-color: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            color: #c7254e;
        }}
        
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-left: 4px solid #3498db;
            border-radius: 3px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            page-break-inside: avoid;
        }}
        
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            background-color: #fff;
        }}
        
        table, th, td {{
            border: 1px solid #bdc3c7;
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        
        td {{
            padding: 10px;
        }}
        
        tr:nth-child(even) {{
            background-color: #ecf0f1;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin: 15px 0;
            color: #666;
            font-style: italic;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        
        .page-break {{
            page-break-after: always;
        }}
        
        strong {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        em {{
            font-style: italic;
            color: #555;
        }}
        
        @media print {{
            body {{ padding: 20px; }}
            h1, h2, h3 {{ page-break-after: avoid; }}
            pre {{ page-break-inside: avoid; }}
            table {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
        
        print("📄 Gerando PDF...")
        HTML(string=html_final).write_pdf('DOCUMENTACAO_COMPLETA.pdf')
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Executa o gerador de PDF"""
    print("=" * 70)
    print("🛰️  GERADOR DE PDF - DOCUMENTAÇÃO DO SISTEMA")
    print("=" * 70)
    print()
    
    md_file = Path('DOCUMENTACAO_COMPLETA.md')
    pdf_file = Path('DOCUMENTACAO_COMPLETA.pdf')
    
    # Verificar se MD existe
    if not md_file.exists():
        print(f"❌ Arquivo não encontrado: {md_file}")
        return False
    
    print(f"✅ Arquivo encontrado: {md_file}")
    print(f"📊 Tamanho: {md_file.stat().st_size / 1024:.1f} KB")
    print()
    
    # Tentar métodos na ordem de preferência
    print("Tentando método 1: Pandoc...")
    if gerar_pdf_com_pandoc():
        print("✅ PDF gerado com Pandoc!")
    else:
        print("⚠️  Pandoc não disponível, tentando WeasyPrint...")
        if gerar_pdf_com_weasyprint():
            print("✅ PDF gerado com WeasyPrint!")
        else:
            print("❌ Todos os métodos falharam")
            return False
    
    # Verificar resultado
    if pdf_file.exists():
        tamanho_mb = pdf_file.stat().st_size / (1024 * 1024)
        print()
        print("=" * 70)
        print("✨ SUCESSO!")
        print("=" * 70)
        print(f"📁 Arquivo: {pdf_file.absolute()}")
        print(f"📊 Tamanho: {tamanho_mb:.2f} MB")
        print()
        print("O PDF está pronto para ser consultado ou impresso!")
        return True
    else:
        print("❌ PDF não foi criado")
        return False

if __name__ == '__main__':
    sucesso = main()
    sys.exit(0 if sucesso else 1)
