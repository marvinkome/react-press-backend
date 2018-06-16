from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
socket = SocketIO()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    DATABASE_URI = getattr(app.config, 'SQLALCHEMY_DATABASE_URI', '')
    is_sqlite = DATABASE_URI.startswith('sqlite:')
    migrate.init_app(app, db, render_as_batch=is_sqlite)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={"*": {"origins": app.config['CLIENT_SIDE_ORIGIN']}})
    socket.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
