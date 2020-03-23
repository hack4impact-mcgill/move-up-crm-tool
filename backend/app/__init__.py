from flask import Flask
from flask_mail import Mail
from config import config
from flask_cors import CORS

mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # set up Flask Mail extension
    mail.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
