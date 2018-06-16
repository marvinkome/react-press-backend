import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError
from flask_jwt_extended import get_jwt_identity

from ..model import (
    Clap as ClapModel, 
    User as UserModel, 
    Post as PostModel,
    Notification as NotificationModel
)
from .. import db, socket
from ..helpers import get_unread_notifications
from .post import Post
from .helpers import CustomSQLAlchemyObjectType

class Clap(CustomSQLAlchemyObjectType):
    class Meta:
        model = ClapModel
        interfaces = (relay.Node, )

class CreateClap(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)

    post = graphene.Field(lambda: Post)

    def mutate(self, info, post_id):
        post = PostModel.query.filter_by(uuid=post_id).first()

        email = get_jwt_identity()
        if email is None:
            return GraphQLError('You need an access token to perform this action')

        user = UserModel.query.filter_by(email=email).first()

        clap = ClapModel()
        notification = NotificationModel()

        if post is not None and user is not None:
            clap.post_id = post_id
            clap.author_id = user.uuid
            db.session.add(clap)

            # set emit to false by default
            emit = False

            # create new notification only if user has not clapped before
            user_claps = NotificationModel.query.filter_by(from_author=user, type='clapped').count()
            if user_claps == 0:
                notification.author_id = post.author.uuid
                notification.post_id = post.uuid
                notification.from_author_id = user.uuid
                notification.type = 'clapped'
                db.session.add(notification)
                emit = True

            db.session.commit()

        if emit is True:
            socket.emit(
                'notifications', 
                get_unread_notifications(post.author), 
                room=post.author.session_id, 
                broadcast=False
            )
            
        return CreateClap(post=post)
