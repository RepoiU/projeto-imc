from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import bp as imc_bp
    app.register_blueprint(imc_bp)

    return app
