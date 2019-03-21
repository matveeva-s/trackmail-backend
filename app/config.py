class Config(object):
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://svetlana:123@localhost/base"
    TESTING = True
    DB_NAME = "base"
    DB_HOST = "localhost"
    DB_USER = "svetlana"
    DB_PASS = "123"


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://svetlana:123@localhost/base"
    TESTING = True
    DEBUG = True
    DB_NAME = "base"
    DB_HOST = "localhost"
    DB_USER = "svetlana"
    DB_PASS = "123"
