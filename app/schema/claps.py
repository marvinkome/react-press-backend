import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError
from flask_jwt_extended import get_jwt_identity

from ..model import Clap as ClapModel, User as UserModel, Post as PostModel
from .. import db
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

        if post is not None and user is not None:
            clap.post_id = post_id
            clap.author_id = user.uuid

        db.session.add(clap)
        db.session.commit()
        return CreateClap(post=post)
