from .. import db
from ..helpers import generate_graphql_token
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notification'

    uuid = db.Column(db.Integer, primary_key=True)
    read = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(32), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.uuid'))
    from_author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))

    def to_json(self):
        return {
            'uuid': self.uuid,
            'id': generate_graphql_token('Notification', self.uuid),
            'from': {
                'uuid': self.from_author.uuid,
                'name': self.from_author.full_name,
                'id': generate_graphql_token('User', self.from_author.uuid)
            },
            'post': {
                'uuid': self.post.uuid,
                'title': self.post.title,
                'id': generate_graphql_token('Post', self.post.uuid)
            },
            'timestamp': self.timestamp.isoformat(),
            'type': self.type,
            'read': self.read
        }

    def __repr__(self):
        return '<Notification %r>' % self.uuid