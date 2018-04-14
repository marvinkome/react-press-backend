from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..model import User as UserModel

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

