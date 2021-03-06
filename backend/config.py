import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = "Move Up CRM Tool"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = str(os.environ.get("DEV_AIRTABLE_URL"))


class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = str(os.environ.get("TEST_AIRTABLE_URL"))


class ProductionConfig(Config):
    PRODUCTION = True
    DATABASE_URL = str(os.environ.get("PROD_AIRTABLE_URL"))


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
