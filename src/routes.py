from flask import Blueprint, request, jsonify, render_template
import traceback
import requests

from .pdf_utils import gerar_pdf
from .email_utils import enviar_email
from .templates_email import template_email
from .helpers import formatar_numero

bp = Blueprint("imc", __name__)

# 🔑 Chave secreta do Google reCAPTCHA
SECRET_KEY = "6Lcqd90rAAAAACt6GxbIs2GUX3HC5jRCqwfQc427"


@bp.route("/calculo", methods=["POST"])
def calculo():
    try:
        # 🔍 Tenta capturar tanto JSON quanto form-data
        data = request.get_json(silent=True) or request.form.to_dict()

        recaptcha_response = data.get("g-recaptcha-response")
        if not recaptcha_response:
            return jsonify({"status": "erro", "mensagem": "reCAPTCHA não enviado"}), 400

        # ✅ Verifica o token com o Google
        verify = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": SECRET_KEY, "response": recaptcha_response},
            timeout=5
        ).json()

        if not verify.get("success"):
            return jsonify({"status": "erro", "mensagem": "Verificação reCAPTCHA falhou"}), 400

        # 🔹 Captura e valida os dados do usuário
        nome = (data.get("nome") or "").strip()
        sobrenome = (data.get("sobrenome") or "").strip()
        cidade = (data.get("cidade") or "").strip()
        numero = formatar_numero((data.get("numero") or "").strip())
        email = (data.get("email") or "").strip()
        altura = str(data.get("altura") or "").replace(",", ".").strip()
        peso = str(data.get("peso") or "").replace(",", ".").strip()

        if not altura or not peso:
            return jsonify({"status": "erro", "mensagem": "Peso ou altura não informados"}), 400

        try:
            altura = float(altura)
            peso = float(peso)
        except ValueError:
            return jsonify({"status": "erro", "mensagem": "Peso e altura precisam ser numéricos"}), 400

        # 📄 Gera PDF com resultado
        arquivo_pdf, filename, imc, classificacao, recomendacao = gerar_pdf(
            nome, sobrenome, cidade, numero, email, peso, altura
        )

        # ✉️ Envia e-mail bonito com o relatório
        assunto = "Seu Relatório de IMC"
        conteudo = template_email(nome, imc, classificacao, recomendacao)
        enviado = enviar_email(email, assunto, conteudo, arquivo_pdf, filename)

        if not enviado:
            return jsonify({"status": "erro", "mensagem": "Falha ao enviar o e-mail."}), 502

        # ✅ Renderiza a tela de sucesso
        return render_template("sucesso.html")

    except Exception as e:
        print("❌ ERRO INTERNO:", e)
        return jsonify({
            "status": "erro",
            "mensagem": "Erro interno no servidor.",
            "trace": traceback.format_exc()
        }), 500


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/sucesso", methods=["GET"])
def sucesso():
    return render_template("sucesso.html")
