import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..model import Tags as TagModel, Post as PostModel
from .. import db

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

    tag = graphene.Field(lambda: Tags)
    def mutate(self, info, tag_data = None):
        post = PostModel.query.filter_by(uuid=tag_data.post_id).first()
        print(post)
        tag = TagModel(name=tag_data.name)
        tag.posts.append(post)

        db.session.add(tag)
        db.session.commit()
        return CreateTag(tag=tag)
