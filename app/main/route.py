import re
import os

from flask import make_response, request, jsonify, url_for, send_from_directory, current_app as app
from flask_graphql import GraphQLView

from flask_jwt_extended import (jwt_required, jwt_optional, set_access_cookies, unset_jwt_cookies,
    create_access_token, create_refresh_token, get_jwt_identity, set_refresh_cookies,
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
        graphiql=True # for having the GraphiQL interface
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

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    resp = jsonify({
        'msg': 'Authentication successfull',
        'login': True
    })
    
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp

@main.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    full_name = request.json.get('full_name')
    password = request.json.get('password')

    if (validate_password(password) is False):
        return jsonify({
            'msg': 'Password is not valid',
            'access_token': None,
            'refresh_token': None
        });

    user = User(
        email=email,
        full_name=full_name,
        password=password
    )
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    resp = jsonify({
        'msg': 'Authentication successfull',
        'login': True
    })
    
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    
    return resp

@main.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    print(request.cookies)
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = jsonify({
        'msg': 'refreshed'
    })
    set_access_cookies(ret, access_token)
    return ret

@main.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

@main.route('/', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({
                'msg': 'no file part'
            })
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'msg': 'no selected file'
            })
        if file and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({
                'msg': 'file uploaded',
                'url': url_for('main.uploaded_file', filename=filename)
            })
    return jsonify({
        'msg': 'This is the upload path'
    })

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app.config['FLASKY_DB_QUERY_TIMEOUT']:
            app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
                (query.statement, query.parameters, query.duration, query.context))
    return response
