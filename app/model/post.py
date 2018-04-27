from flask import current_app
from datetime import datetime
from .. import db
from .tags import TagsRelationship
from .user import User

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

    @staticmethod
    def generate_fake(count=10):
        from random import seed, randint
        import forgery_py
        
        seed()
        user_count = User.query.count()
        
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(
                title=forgery_py.lorem_ipsum.title(3),
                body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                timestamp=forgery_py.date.date(True),
                post_pic_url='192.168.43.200:5000/uploads/Curso-React.js-Ninja-Modulo-React-Webpack.jpg',
                author=u
            )

            db.session.add(p)
            db.session.commit()

    def __repr__(self):
        return '<Post %r>' % self.title
