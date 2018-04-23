import re
import os
from flask import request, jsonify, url_for, send_from_directory, current_app as app
from flask_graphql import GraphQLView
from flask_jwt_extended import (jwt_required,
    create_access_token, create_refresh_token, get_jwt_identity,
    jwt_refresh_token_required)
from werkzeug.utils import secure_filename
from . import main
from .. import db, jwt
from ..model import User
from ..schema import schema

main.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
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
    
    return jsonify({
        'msg': 'Authentication successfull',
        'access_token': access_token,
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
    return jsonify({
        'msg': 'Profile Created',
        'access_token': access_token,
        'refresh_token': refresh_token
    })

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

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
