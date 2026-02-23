import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # You can also override it specifically here if you prefer
    # SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

class ProductionConfig(BaseConfig):
    DEBUG = False
    # In production, you'd want to FORCE an error if the URL is missing
    # so the app doesn't accidentally start with a local SQLite file.
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        url = os.getenv("DATABASE_URL")
        if not url:
            raise ValueError("No DATABASE_URL set for Production environment")
        return url

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig  # Don't forget to add testing to the map!
}