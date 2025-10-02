from flask import Blueprint, request, jsonify, render_template, send_from_directory
from urllib.parse import urljoin, quote
import traceback
import base64
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

from .pdf_utils import gerar_pdf
from .helpers import formatar_numero

bp = Blueprint("imc", __name__)

@bp.route("/calculo", methods=["POST"])
def calculo():
    try:
        data = request.get_json(force=True)

        nome = data.get("nome", "").strip()
        sobrenome = data.get("sobrenome", "").strip()
        cidade = data.get("cidade", "").strip()
        numero = formatar_numero(data.get("numero", "").strip())
        email = data.get("email", "").strip()
        altura = str(data.get("altura", "")).replace(",", ".").strip()
        peso = str(data.get("peso", "")).replace(",", ".").strip()

        if not altura or not peso:
            return jsonify({"status": "erro", "mensagem": "Peso ou altura não informados"}), 400

        try:
            altura = float(altura)
            peso = float(peso)
        except ValueError:
            return jsonify({"status": "erro", "mensagem": "Peso e altura precisam ser numéricos"}), 400

        # gera pdf
        arquivo_pdf, filename, imc, classificacao, recomendacao = gerar_pdf(
            nome, sobrenome, cidade, numero, email, peso, altura
        )

        # envia por email
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            from_email = os.environ.get("EMAIL_SENDER")
            to_email = email

            with open(arquivo_pdf, "rb") as f:
                file_data = f.read()
                encoded_file = base64.b64encode(file_data).decode()

            attachment = Attachment(
                FileContent(encoded_file),
                FileName(filename),
                FileType("application/pdf"),
                Disposition("attachment")
            )

            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject="Seu Relatório de IMC",
                html_content=f"""
                <p>Olá <b>{nome}</b>,</p>
                <p>Segue em anexo o seu relatório de IMC.</p>
                <p><b>IMC:</b> {imc} ({classificacao})</p>
                <p><b>Recomendação:</b> {recomendacao}</p>
                <br>
                <p>Atenciosamente, <br>Equipe Novatra</p>
                """
            )
            message.attachment = attachment
            sg.send(message)

        except Exception as e:
            print("⚠️ Erro ao enviar email:", e)

        # URL pública do arquivo
        base_url = request.url_root
        file_url = urljoin(base_url, f"arquivo/{quote(filename)}")

        # renderiza a página de sucesso passando o link para download
        return render_template("sucesso.html", file_url=file_url)

    except Exception:
        return jsonify({
            "status": "erro",
            "mensagem": "Erro interno",
            "trace": traceback.format_exc()
        }), 500


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/sucesso", methods=["GET"])
def sucesso():
    # se abrir direto /sucesso sem passar file_url, não quebra
    return render_template("sucesso.html", file_url=None)


# 🔥 Nova rota para servir os relatórios PDF
@bp.route("/arquivo/<path:filename>", methods=["GET"])
def download(filename):
    pasta_resultados = os.path.join(os.path.dirname(__file__), "resultados")
    return send_from_directory(pasta_resultados, filename, as_attachment=True)
