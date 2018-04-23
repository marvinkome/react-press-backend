from flask import current_app
from datetime import datetime
from .. import db
from .tags import TagsRelationship

class Post(db.Model):
    __tablename__ = 'posts'

    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_pic_url = db.Column(db.String(128))

    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))

    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    claps = db.relationship('Clap', backref='post', lazy='dynamic')
    tags = db.relationship('Tags',
                        secondary=TagsRelationship,
                        backref=db.backref('posts', lazy='dynamic'),
                        lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.title
