import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError
from flask_jwt_extended import get_jwt_identity

from ..model import Tags as TagModel, Post as PostModel
from .. import db
from .post import Post

class Tags(SQLAlchemyObjectType):
    class Meta:
        model = TagModel
        interfaces = (relay.Node, )

class TagInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    post_id = graphene.Int(required=True)

class CreateTag(graphene.Mutation):
    class Arguments:
        tag_data = TagInput(required=True)

    post = graphene.Field(lambda: Post)
    def mutate(self, info, tag_data = None):
        email = get_jwt_identity()
        if email is None:
            return GraphQLError('You need an access token to perform this action')

        post = PostModel.query.filter_by(uuid=tag_data.post_id).first()
        
        tag = TagModel(name=tag_data.name)
        tag.posts.append(post)

        db.session.add(tag)
        db.session.commit()
        return CreateTag(post=post)
