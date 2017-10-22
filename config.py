import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Atlant@localhost/bcore?charset=utf8'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    UPLOAD_FOLDER = '/static/img/picturs'

@staticmethod
def init_app(app):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': TestingConfig,
}
