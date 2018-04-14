from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..model import Post as PostModel

class Post(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (relay.Node, )

