class Config(object):
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://svetlana:123@localhost/chat_base"
    TESTING = True
    DB_NAME = "chat_base"
    DB_HOST = "localhost"
    DB_USER = "svetlana"
    DB_PASS = "123"


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://svetlana:123@localhost/chat_base"
    TESTING = True
    DEBUG = True
    DB_NAME = "chat_base"
    DB_HOST = "localhost"
    DB_USER = "svetlana"
    DB_PASS = "123"
