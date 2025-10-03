from flask import Flask
from src import routes  # importa o blueprint

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",   # HTMLs
        static_folder="../static"        # CSS, JS, imagens
    )
    app.register_blueprint(routes.bp)  # registra o blueprint
    return app

# 🔹 Instância global (Render/Gunicorn precisa disso)
app = create_app()

# 🔹 Só roda assim localmente
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
