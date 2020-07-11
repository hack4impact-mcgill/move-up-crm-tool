from flask import Flask
from flask_mail import Mail
import os
from flask_cors import CORS
from config import config

mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)

    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG") or "default"

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # set up Flask Mail extension
    mail.init_app(app)

    # create app blueprint
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
