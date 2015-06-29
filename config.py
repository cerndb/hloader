import os

class Config(object):
    DEBUG = False
    ORACLE_DATABASE_URI = os.environ.get('ORACLE_DATABASE_URI', None)

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', None)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/hloader-db'
