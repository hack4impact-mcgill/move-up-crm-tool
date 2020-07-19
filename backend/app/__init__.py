from flask import Flask
from flask_mail import Mail
import os
from flask_cors import CORS
from config import config
from flask_jwt_extended import JWTManager

mail = Mail()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app,
         supports_credentials=True,
         resources={
             r"/*": {
                 "origins": [
                     r"http://localhost:*",
                     r"http://127.0.0.1:*",
                     r"http://192.168.0.11:*",
                 ]
             }
         },)

    # get config from env
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG") or "default"

    # set up JWT cookie management
    app.config.from_object(config[config_name])
    # app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    # app.config["JWT_CSRF_IN_COOKIES"] = True
    # # True if config_name == "production" else False
    # # app.config["JWT_COOKIE_SECURE"] = False
    # # if config_name == "testing" else True
    # app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    # app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = True if config_name == "production" else False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False if config_name == "testing" else True
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]

    config[config_name].init_app(app)

    jwt.init_app(app)

    # set up Flask Mail extension
    mail.init_app(app)

    # create app blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
