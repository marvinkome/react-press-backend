from .. import db
from datetime import datetime

class Clap(db.Model):
    __tablename__ = 'clap'

    uuid = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.uuid'))

    def __repr__(self):
        return '<Clap %r>' % self.uuid
