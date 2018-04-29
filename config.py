# ./config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://postgres:123456@localhost/'
database_name = 'api'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # Todo

    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # Todo

    JWT_TOKEN_LOCATION = 'cookies'
    JWT_COOKIE_SECURE = False # Todo
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True # Todo

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True

    CORS_SUPPORTS_CREDENTIALS = True

    UPLOAD_FOLDER = os.path.join(basedir + '/', 'file_uploads/')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    FLASKY_DB_QUERY_TIMEOUT = 0.5

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', postgres_local_base + database_name)
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
    
        # # email errors to the administrators
        # import logging
        # from logging.handlers import SMTPHandler
        
        # credentials = None
        # secure = None
        # if getattr(cls, 'MAIL_USERNAME', None) is not None:
        #     credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
        #     if getattr(cls, 'MAIL_USE_TLS', None):
        #         secure = ()
            
        #     mail_handler = SMTPHandler(
        #                         mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
        #                         fromaddr=cls.FLASKY_MAIL_SENDER,
        #                         toaddrs=[cls.FLASKY_ADMIN],
        #                         subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
        #                         credentials=credentials,
        #                         secure=secure)

        #     mail_handler.setLevel(logging.ERROR)
        #     app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}