import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .user import User
from .post import Post
from .comment import Comment

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    users = graphene.List(User)
    posts = graphene.List(Post)
    comments = graphene.List(Comment)
    post = graphene.Field(Post, uuid=graphene.Int())

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_posts(self, info):
        query = Post.get_query(info)
        return query.all()

    def resolve_comments(self, info):
        query = Comment.get_query(info)
        return query.all()

    def resolve_post(self, info, uuid):
        query = Post.get_query(info)
        return query.get(uuid)

schema = graphene.Schema(query=Query, types=[User, Post])
