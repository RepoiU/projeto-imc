from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
from datetime import datetime
import io
import os

from .imc_utils import calcular_imc, classificar_imc
from .ibge_utils import buscar_municipio_ibge
from .helpers import _paths


def gerar_pdf(nome, sobrenome, cidade, numero, email, peso, altura):
    base_dir, pasta_resultados, template = _paths()

    imc = calcular_imc(peso, altura)
    classificacao, recomendacao = classificar_imc(imc)

    cidade_com_uf = buscar_municipio_ibge(cidade)
    if cidade_com_uf:
        cidade = cidade_com_uf

    # carrega template
    with open(template, "rb") as f:
        template_pdf = PdfReader(f)
        page = template_pdf.pages[0]
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

    # escreve sobre template
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFont("Helvetica", 12)

    c.drawString(90, 321, nome)
    c.drawString(120, 291, sobrenome)
    c.drawString(100, 261, cidade)
    c.drawString(100, 231, numero)
    c.drawString(90, 201, email)

    c.drawString(90, 171, f"{peso} kg")
    c.drawString(90, 141, f"{altura} m")
    c.drawString(80, 111, f"{imc} ({classificacao})")

    c.drawString(50, 81, f"Recomendação: {recomendacao}")

    c.save()
    packet.seek(0)

    overlay_pdf = PdfReader(packet)
    output_pdf = PdfWriter()

    with open(template, "rb") as f:
        template_pdf = PdfReader(f)
        for i, page in enumerate(template_pdf.pages):
            if i == 0:
                page.merge_page(overlay_pdf.pages[0])
            output_pdf.add_page(page)

    # salva arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{nome}_{timestamp}_relatorio.pdf"
    arquivo = os.path.join(pasta_resultados, filename)

    with open(arquivo, "wb") as f_out:
        output_pdf.write(f_out)

    return arquivo, filename, imc, classificacao, recomendacao
