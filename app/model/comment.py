from .. import db
from .user import User
from .post import Post
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    uuid = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.uuid'))

    replies = db.relationship('CommentReply', backref='parent', lazy='dynamic')

    @staticmethod
    def generate_fake(count=5):
        from random import seed, randint
        import forgery_py
        
        seed()
        user_count = User.query.count()
        post_count = Post.query.count()
        
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post.query.offset(randint(0, post_count - 1)).first()
            c = Comment(
                body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                timestamp=forgery_py.date.date(True),
                author=u,
                post=p
            )

            db.session.add(c)
            db.session.commit()

    def __repr__(self):
        return '<Comment %r>' % self.uuid

class CommentReply(db.Model):
    __tablename__ = 'comments_reply'

    uuid = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.uuid'))

    @staticmethod
    def generate_fake(count=5):
        from random import seed, randint
        import forgery_py
        
        seed()
        user_count = User.query.count()
        comment_count = Comment.query.count()

        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            c = Comment.query.offset(randint(0, comment_count - 1)).first()
            cr = CommentReply(
                body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                timestamp=forgery_py.date.date(True),
                author=u,
                parent=c
            )

            db.session.add(cr)
            db.session.commit()

    def __repr__(self):
        return '<CommentReply to="{0}" id="{1}">'.format(self.parent_id, self.uuid)