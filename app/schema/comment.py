from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..model import Comment as CommentModel, CommentReply as CommentReplyModel

class Comment(SQLAlchemyObjectType):
    class Meta:
        model = CommentModel
        interfaces = (relay.Node, )

class CommentReply(SQLAlchemyObjectType):
    class Meta:
        model = CommentReplyModel
        interfaces = (relay.Node, )
