import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
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
        user_id = graphene.Int(required=True)

    post = graphene.Field(lambda: Post)

    def mutate(self, info, post_id, user_id):
        post = PostModel.query.filter_by(uuid=post_id).first()
        user = UserModel.query.filter_by(uuid=user_id).first()

        clap = ClapModel()

        if post is not None and user is not None:
            clap.post_id = post_id
            clap.author_id = user_id

        db.session.add(clap)
        db.session.commit()
        return CreateClap(post=post)
