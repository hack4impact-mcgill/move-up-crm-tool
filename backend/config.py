import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = "Move Up CRM Tool"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"

    # Email
    EMAIL_SENDER = "hack4impactmcgilltest@gmail.com"
    EMAIL_SUBJECT_PREFIX = "[{}]".format(APP_NAME)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = os.environ.get("MAIL_PORT", 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", True)
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", False)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
