from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..model import Clap as ClapModel

class Clap(SQLAlchemyObjectType):
    class Meta:
        model = ClapModel
        interfaces = (relay.Node, )

