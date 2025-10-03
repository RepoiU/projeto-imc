from flask import Blueprint, request, jsonify, render_template
import traceback

from .pdf_utils import gerar_pdf
from .email_utils import enviar_email
from .templates_email import template_email   # importa o template aqui
from .helpers import formatar_numero

bp = Blueprint("imc", __name__)

@bp.route("/calculo", methods=["POST"])
def calculo():
    try:
        data = request.get_json(force=True)

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

        # 📄 Gera o PDF correto (abaixo, normal, sobrepeso, obesidade)
        arquivo_pdf, filename, imc, classificacao, recomendacao = gerar_pdf(
            nome, sobrenome, cidade, numero, email, peso, altura
        )

        # ✉️ Envia e-mail (usando o template bonito)
        assunto = "Seu Relatório de IMC"
        conteudo = template_email(nome, imc, classificacao, recomendacao)   # <<< aqui
        enviado = enviar_email(email, assunto, conteudo, arquivo_pdf, filename)

        if not enviado:
            return jsonify({"status": "erro", "mensagem": "Não foi possível enviar o e-mail agora."}), 502

        # ✅ Tela de sucesso (sem link de download)
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
