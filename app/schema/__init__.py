import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from flask_jwt_extended import decode_token
from .user import User
from .post import Post
from .comment import Comment

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    users = graphene.List(User)
    user = graphene.Field(User, uuid=graphene.Int())
    posts = graphene.List(Post)
    comments = graphene.List(Comment)

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_posts(self, info):
        query = Post.get_query(info)
        return query.all()

    def resolve_comments(self, info):
        query = Comment.get_query(info)
        return query.all()

    def resolve_user(self, info):
        query = User.get_query(info)
        token = info.context.headers.get('AUTHORIZATION')
        token_type = decode_token(token)["type"]
        email = None
        if token_type == 'access':
            email = decode_token(token)['identity']
        # print(dir(query))
        return query.filter_by(email=email).first()

schema = graphene.Schema(query=Query, types=[User, Post])
schema.execute('THE QUERY', middleware=[])
