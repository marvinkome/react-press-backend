import re
import os

from flask import make_response, request, jsonify, url_for, send_from_directory, current_app as app
from flask_graphql import GraphQLView

from flask_jwt_extended import (jwt_required, jwt_optional,
    create_access_token, create_refresh_token, get_jwt_identity,
    jwt_refresh_token_required)

from werkzeug.utils import secure_filename
from flask_sqlalchemy import get_debug_queries
from . import main
from .. import db, jwt
from ..model import User
from ..schema import schema

def graphql():
    g = GraphQLView.as_view(
        'graphql',
        schema=schema,
        context={'session': db.session},
        graphiql=False # for having the GraphiQL interface
    )
    return jwt_optional(g)

main.add_url_rule(
    '/graphql',
    view_func=graphql()
)

def validate_password(password):
    regExp = re.compile('^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|\
                        ((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})')
    r = regExp.match(password)
    if (r is not None):
        return True
    else:
        return False

def allowed_filename(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@main.route('/login', methods=['POST','GET'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            'msg': 'Email isn\'t correct. Please Check again',
            'access_token': None,
            'refresh_token': None
        })
    
    check_psw = user.verify_password(password)
    if not check_psw:
        return jsonify({
            'msg': 'password isn\'t correct. Please Check again',
            'access_token': None,
            'refresh_token': None
        })

    refresh_token = create_refresh_token(identity=user.email)

    return jsonify({
        'msg': 'Authentication successfull',
        'login': True,
        'refresh_token': refresh_token
    })

@main.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    full_name = request.json.get('full_name')
    password = request.json.get('password')

    if (validate_password(password) is False):
        return jsonify({
            'msg': 'Password is not valid',
            'login': False,
            'refresh_token': None
        })

    # Check if user exists
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            'msg': 'Email has been taken, please use a different email or login',
            'login': False,
            'refresh_token': None
        })

    user = User(
        email=email,
        full_name=full_name,
        password=password
    )
    db.session.add(user)
    db.session.commit()

    refresh_token = create_refresh_token(identity=user.email)

    return jsonify({
        'msg': 'Authentication successfull',
        'login': True,
        'refresh_token': refresh_token
    })

@main.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({
        'refreshed': True,
        'access_token': access_token
    })

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app.config['FLASKY_DB_QUERY_TIMEOUT']:
            app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
                (query.statement, query.parameters, query.duration, query.context))
    return response
