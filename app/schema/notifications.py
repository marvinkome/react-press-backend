from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..model import Notification as NotificationModel

class Notification(SQLAlchemyObjectType):
    class Meta:
        model = NotificationModel
        interfaces = (relay.Node, )
