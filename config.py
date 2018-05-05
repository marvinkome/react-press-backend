# ./config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
mydir = os.path.dirname(__file__)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # Todo
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # Todo
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_DB_QUERY_TIMEOUT = 0.5
    SSL_DISABLE = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    CLIENT_SIDE_ORIGIN = 'http://192.168.43.200:8080' # Change this if contributing

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    CLIENT_SIDE_ORIGIN = 'http://192.168.43.200:8080' # Change this if contributing

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))
    CLIENT_SIDE_ORIGIN = 'https://reactpress.herokuapp.com'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)
        
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}