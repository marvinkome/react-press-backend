import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .user import User
from .post import Post

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_user = graphene.List(User)
    all_post = graphene.List(Post)

    def resolve_all_user(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_all_post(self, info):
        query = Post.get_query(info)
        return query.all()

schema = graphene.Schema(query=Query, types=[User, Post])