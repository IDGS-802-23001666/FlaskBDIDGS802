import os

class Config(object):
    SECRET_KEY = 'Clave Nueva'
    SESSION_COOKIE_SECURE = False

# 1. Corregimos el nombre a DevelopmentConfig
class DevelopmentConfig(Config):
    DEBUG = True
    # 2. Corregimos URL por URI (esto es vital)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:a1006@127.0.0.1/idgs802'
    SQLALCHEMY_TRACK_MODIFICATIONS = False