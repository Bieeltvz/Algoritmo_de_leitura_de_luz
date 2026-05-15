from fpdf import FPDF
import os

def create_pdf(input_md, output_pdf):
    if not os.path.exists(input_md):
        print(f"Error: {input_md} not found")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(input_md, "r", encoding="utf-8") as f:
        for line in f:
            # Simple sanitization for FPDF (removes characters it might not handle well in default fonts)
            clean_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=clean_line)
    
    pdf.output(output_pdf)
    print(f"✅ PDF created: {output_pdf}")

if __name__ == "__main__":
    create_pdf("DOCUMENTACAO_COMPLETA.md", "DOCUMENTACAO_LEITURA_LUZ.pdf")
