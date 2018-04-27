import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..model import Post as PostModel, User as UserModel
from .. import db
from .helpers import CustomSQLAlchemyObjectType

class Post(CustomSQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (relay.Node, )

class PostInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    body = graphene.String(required=True)
    user_id = graphene.Int(required=True)
    post_pic_url = graphene.String()

class CreatePost(graphene.Mutation):
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(lambda: Post)

    def mutate(self, info, post_data = None):
        user = UserModel.query.filter_by(uuid=post_data.user_id).first()
        if post_data.post_pic_url is not None:
            post = PostModel(
                title=post_data.title,
                body=post_data.body,
                post_pic_url=post_data.post_pic_url
            )
        else:
            post = PostModel(
                title=post_data.title,
                body=post_data.body
            )

        post.author = user

        db.session.add(post)
        db.session.commit()
        return CreatePost(post=post)

class UpdatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        body = graphene.String()
        post_pic_url = graphene.String()
        post_id = graphene.Int(required=True)

    post = graphene.Field(lambda: Post)

    def mutate(self, info, post_id, title=None, body=None, post_pic_url=None):
        post = PostModel.query.filter_by(uuid=post_id).first()
        if post is not None:
            if title is not None:
                post.title = title
            if body is not None:
                post.body = body
            if post_pic_url is not None:
                post.post_pic_url = post_pic_url
            
        db.session.add(post)
        db.session.commit()
        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)

    post = graphene.Field(lambda: Post)

    def mutate(self, info, post_id):
        post = PostModel.query.filter_by(uuid=post_id).first()
        if post is not None:
            db.session.delete(post)
            db.session.commit()
        
        return DeletePost(post=post)