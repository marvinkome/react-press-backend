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
    gravatar_url = db.Column(db.String(256))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    comment_replies = db.relationship('CommentReply', backref='author', lazy='dynamic')
    claps = db.relationship('Clap', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        
        seed()
        for i in range(count):
            u = User(
                    email=forgery_py.internet.email_address(),
                    password=forgery_py.lorem_ipsum.word(),
                    full_name=forgery_py.name.full_name(),
                    description=forgery_py.lorem_ipsum.sentence(),
                    member_since=forgery_py.date.date(True)
                )
            db.session.add(u)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<User %r>' % self.email
