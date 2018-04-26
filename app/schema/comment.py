import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..model import (
    Comment as CommentModel, 
    CommentReply as CommentReplyModel, 
    Post as PostModel,
    User as UserModel
)
from .. import db
from .post import Post

class Comment(SQLAlchemyObjectType):
    class Meta:
        model = CommentModel
        interfaces = (relay.Node, )

class CommentReply(SQLAlchemyObjectType):
    class Meta:
        model = CommentReplyModel
        interfaces = (relay.Node, )


class CreateComment(graphene.Mutation):
    class Arguments:
        body = graphene.String(required=True)
        post_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    post = graphene.Field(lambda: Post)
    comment = graphene.Field(lambda: Comment)

    def mutate(self, info, body, post_id, user_id):
        post = PostModel.query.filter_by(uuid=post_id).first()
        user = UserModel.query.filter_by(uuid=user_id).first()

        comment = CommentModel()

        if post is not None and user is not None:
            comment.body = body
            comment.post_id = post_id
            comment.author_id = user_id

        db.session.add(comment)
        db.session.commit()
        return CreateComment(post=post, comment=comment)

class CreateReplyComment(graphene.Mutation):
    class Arguments:
        body = graphene.String(required=True)
        parent_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    post = graphene.Field(lambda: Post)
    commentReply = graphene.Field(lambda: CommentReply)

    def mutate(self, info, body, parent_id, user_id):
        parent = CommentModel.query.filter_by(uuid=parent_id).first()
        user = UserModel.query.filter_by(uuid=user_id).first()
        post = parent.post

        comment_reply = CommentReplyModel()

        if parent is not None and user is not None:
            comment_reply.body = body
            comment_reply.parent_id = parent_id
            comment_reply.author_id = user_id

        db.session.add(comment_reply)
        db.session.commit()
        return CreateReplyComment(post=post, commentReply=comment_reply)
