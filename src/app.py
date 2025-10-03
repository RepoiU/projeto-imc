from flask import Flask
from src import routes
import requests
from flask import request, jsonify

SECRET_KEY = "6Lcqd90rAAAAACt6GxbIs2GUX3HC5jRCqwfQc427"

@bp.route("/calculo", methods=["POST"])
def calculo():
    # Captura o token do reCAPTCHA
    recaptcha_response = request.form.get("g-recaptcha-response") or request.json.get("g-recaptcha-response")
    
    # Valida com Google
    data = {
        'secret': SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    result = r.json()

    if not result.get("success"):
        return jsonify({"mensagem": "Verificação reCAPTCHA falhou"}), 400


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",   # HTMLs
        static_folder="../static"        # CSS, JS, imagens
    )
    app.register_blueprint(routes.bp)
    return app

# 🔹 Instância global (Render/Gunicorn precisa disso)
app = create_app()

# 🔹 Só roda assim localmente
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)