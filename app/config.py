class Config(object):
    TESTING = False


class ProductionConfig(Config):
    TESTING = False
    DB_NAME = "base"
    DB_HOST = "localhost"
    DB_USER = "svetlana"
    DB_PASS = "123"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DB_NAME = "base"
    DB_HOST = "localhost"
    DB_USER = "svetlana"
    DB_PASS = "123"
