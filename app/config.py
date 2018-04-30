class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "5Upp3RS3cR3T"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_SENDER = ''

    DEV_API_KEY = ''

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    MONGODB_DB = 'project_ads'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017


class TestingConfig(Config):
    TESTING = True
