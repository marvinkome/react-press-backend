import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphql import GraphQLError
from flask_jwt_extended import decode_token, get_jwt_identity
from ..model import User as UserModel
from .user import User, UpdateProfilePic, UpdateInfo
from .post import Post, CreatePost, UpdatePost, DeletePost
from .comment import Comment, CreateComment, CreateReplyComment
from .claps import Clap, CreateClap
from .tags import Tags, CreateTag
from .helpers import DescSortAbleConnectionField

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

    create_tag = CreateTag.Field()

    update_user_profile_pic = UpdateProfilePic.Field()
    update_user_info = UpdateInfo.Field()

    create_comment = CreateComment.Field()
    create_comment_reply = CreateReplyComment().Field()

    create_clap = CreateClap.Field()

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    users = graphene.List(User)
    user = graphene.Field(User)
    posts = graphene.List(Post, first=graphene.Int(), skip=graphene.Int())
    all_post = DescSortAbleConnectionField(Post, sort_by=graphene.Argument(graphene.String))
    comments = graphene.List(Comment)

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_posts(self, info, first=None, skip=None):
        query = Post.get_query(info)
        qs = query.all()
        if skip:
            qs = qs[skip::]
        if first:
            qs = qs[:first]
        return qs

    def resolve_comments(self, info):
        query = Comment.get_query(info)
        return query.all()

    def resolve_user(self, info):
        query = User.get_query(info)
        email = get_jwt_identity()
        if email is not None:
            res = query.filter_by(email=email).first()
            if res is None:
                return GraphQLError('Email is invalid')
            return res

        return GraphQLError('You need an Access token to get this data')

schema = graphene.Schema(query=Query, mutation=Mutation, types=[User, Post])
