from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
# from flask_graphql import GraphQL
from config import config

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={"*": {"origin": app.config['CLIENT_SIDE_ORIGIN']}})

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
    