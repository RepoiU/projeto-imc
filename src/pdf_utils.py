from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
from datetime import datetime
import io
import os

from .imc_utils import calcular_imc, classificar_imc
from .ibge_utils import buscar_municipio_ibge
from .helpers import _paths


def draw_debug_grid(c, width, height, step_x=50, step_y=25):
    """
    Desenha uma grade numerada para debug das posições (X,Y).
    """
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    for x in range(0, int(width), step_x):
        c.line(x, 0, x, height)
        c.drawString(x + 2, 5, str(x))
    for y in range(0, int(height), step_y):
        c.line(0, y, width, y)
        c.drawString(5, y + 5, str(y))


def gerar_pdf(nome, sobrenome, cidade, numero, email, peso, altura, debug=False):
    """
    Gera um relatório de IMC com base nos templates e preenche
    automaticamente os dados do cliente na página 2.

    :param nome: Nome do cliente
    :param sobrenome: Sobrenome do cliente
    :param cidade: Cidade do cliente
    :param numero: Número de telefone
    :param email: Email do cliente
    :param peso: Peso em kg
    :param altura: Altura em metros
    :param debug: Se True, desenha a grade de coordenadas no PDF
    :return: caminho do arquivo, nome do arquivo, valor do IMC, classificação e recomendação
    """
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

    hoje = datet
