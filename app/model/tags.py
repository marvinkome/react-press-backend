from flask import jsonify
from .. import db

class Tags(db.Model):
    __tablename__ = 'tags'

    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<Tag %r>' % self.name

TagsRelationship = db.Table('tag-relationship',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.uuid')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.uuid'))
)