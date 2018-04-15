from .. import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    uuid = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.uuid'))

    replies = db.relationship('CommentReply', backref='parent', lazy='dynamic')

    def __repr__(self):
        return '<Comment %r>' % self.uuid

class CommentReply(db.Model):
    __tablename__ = 'comments_reply'

    uuid = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.uuid'))


    def __repr__(self):
        return '<CommentReply to="{0}" id="{1}">'.format(self.parent_id, self.uuid)