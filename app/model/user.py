from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from .. import db
from datetime import datetime
import hashlib

class User(db.Model):
    __tablename__ = 'users'

    uuid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.Text)
    description = db.Column(db.Text)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    gravatar_url = db.Column(db.String(128), unique=True)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    comment_replies = db.relationship('CommentReply', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=259, default='retro', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://wwwp .gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating
        )

    def __repr__(self):
        return '<User %r>' % self.email
