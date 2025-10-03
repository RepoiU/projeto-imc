from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
from datetime import datetime
import io
import os

from .imc_utils import calcular_imc, classificar_imc
from .ibge_utils import buscar_municipio_ibge
from .helpers import _paths


def gerar_pdf(nome, sobrenome, cidade, numero, email, peso, altura):
    base_dir, pasta_resultados, _ = _paths()

    # calcula IMC e classificação
    imc = calcular_imc(peso, altura)
    classificacao, recomendacao = classificar_imc(imc)

    cidade_com_uf = buscar_municipio_ibge(cidade)
    if cidade_com_uf:
        cidade = cidade_com_uf

    # escolhe o template conforme classificação
    if "Abaixo" in classificacao:
        template = os.path.join(base_dir, "templates", "imc_abaixo.pdf")
    elif "Normal" in classificacao:
        template = os.path.join(base_dir, "templates", "imc_normal.pdf")
    elif "Sobrepeso" in classificacao:
        template = os.path.join(base_dir, "templates", "imc_sobrepeso.pdf")
    else:
        template = os.path.join(base_dir, "templates", "imc_obesidade.pdf")

    # carrega template
    reader = PdfReader(template)
    page = reader.pages[1]  # página 2 -> Informações do Cliente
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)

    # escreve sobre a página 2
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFont("Helvetica", 12)

    hoje = datetime.now().strftime("%d/%m/%Y")

    # ajusta posições de acordo com a tabela do PDF (pode ajustar os Y se necessário)
    c.drawString(250, 640, nome)        # Nome
    c.drawString(250, 615, sobrenome)   # Sobrenome
    c.drawString(250, 590, cidade)      # Cidade
    c.drawString(250, 565, numero)      # Número
    c.drawString(250, 540, email)       # Email
    c.drawString(250, 515, f"{peso} kg")
    c.drawString(250, 490, f"{altura} m")
    c.drawString(250, 465, f"{imc} ({classificacao})")
    c.drawString(250, 440, hoje)        # Data da Avaliação

    c.save()
    packet.seek(0)
    overlay_pdf = PdfReader(packet)

    # escreve no PDF final
    output_pdf = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i == 1:  # sobrescreve apenas a página 2
            page.merge_page(overlay_pdf.pages[0])
        output_pdf.add_page(page)

    # salva arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{nome}_{timestamp}_relatorio.pdf"
    arquivo = os.path.join(pasta_resultados, filename)

    with open(arquivo, "wb") as f_out:
        output_pdf.write(f_out)

    return arquivo, filename, imc, classificacao, recomendacao
