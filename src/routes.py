from flask import Blueprint, request, jsonify, render_template, send_file, session, url_for
from urllib.parse import urljoin, quote
import traceback
import base64
import os
import io

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

        # 📄 Gera PDF (em arquivo temporário)
        arquivo_pdf, filename, imc, classificacao, recomendacao = gerar_pdf(
            nome, sobrenome, cidade, numero, email, peso, altura
        )

        # Lê PDF e salva em memória
        with open(arquivo_pdf, "rb") as f:
            pdf_bytes = f.read()

        # Remove arquivo físico (não precisa ficar no servidor)
        try:
            os.remove(arquivo_pdf)
        except:
            pass

        # envia por email
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            from_email = os.environ.get("EMAIL_SENDER")
            to_email = email

            encoded_file = base64.b64encode(pdf_bytes).decode()

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

        # ✅ Salva PDF em sessão
        session["pdf_data"] = base64.b64encode(pdf_bytes).decode()
        session["pdf_name"] = filename

        file_url = url_for("imc.download")
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
    file_url = url_for("imc.download") if "pdf_data" in session else None
    return render_template("sucesso.html", file_url=file_url)


# 🔥 Rota para baixar PDF da sessão
@bp.route("/arquivo/download", methods=["GET"])
def download():
    pdf_data = session.get("pdf_data")
    pdf_name = session.get("pdf_name", "relatorio.pdf")

    if not pdf_data:
        return "Arquivo não encontrado", 404

    buffer = io.BytesIO(base64.b64decode(pdf_data))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=pdf_name, mimetype="application/pdf")
