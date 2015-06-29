import os

class Config(object):
    DEBUG = False
    try:
        ORACLE_DATABASE_URI = os.environ['ORACLE_DATABASE_URI']
    except KeyError:
        print "Error: ORACLE_DATABASE_URI environment variable has " \
              "not been set"

class ProductionConfig(Config):
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    except KeyError:
        print "Error: SQLALCHEMY_DATABASE_URI environment variable has " \
              "not been set"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/hloader-db'
