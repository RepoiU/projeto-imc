from flask import Blueprint, request, jsonify, render_template
import traceback
import requests

from .pdf_utils import gerar_pdf
from .email_utils import enviar_email
from .templates_email import template_email
from .helpers import formatar_numero

bp = Blueprint("imc", __name__)

# 🔑 Sua chave secreta do Google reCAPTCHA
SECRET_KEY = "6Lcqd90rAAAAACt6GxbIs2GUX3HC5jRCqwfQc427"

@bp.route("/calculo", methods=["POST"])
def calculo():
    try:
        # 🔒 Captura o token do reCAPTCHA (JSON ou formulário)
        data = request.get_json(force=True)
        recaptcha_response = data.get("g-recaptcha-response")

        if not recaptcha_response:
            return jsonify({"status": "erro", "mensagem": "reCAPTCHA não enviado"}), 400

        # ✅ Valida no Google
        verify = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": SECRET_KEY, "response": recaptcha_response}
        ).json()

        if not verify.get("success"):
            return jsonify({"status": "erro", "mensagem": "Verificação reCAPTCHA falhou"}), 400

        # 🎯 Continua o fluxo
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

        # 📄 Gera PDF e calcula IMC
        arquivo_pdf, filename, imc, classificacao, recomendacao = gerar_pdf(
            nome, sobrenome, cidade, numero, email, peso, altura
        )

        # ✉️ Envia e-mail
        assunto = "Seu Relatório de IMC"
        conteudo = template_email(nome, imc, classificacao, recomendacao)
        enviado = enviar_email(email, assunto, conteudo, arquivo_pdf, filename)

        if not enviado:
            return jsonify({"status": "erro", "mensagem": "Não foi possível enviar o e-mail agora."}), 502

        # ✅ Página de sucesso
        return render_template("sucesso.html")

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
    return render_template("sucesso.html")
