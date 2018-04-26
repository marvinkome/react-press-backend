import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from flask_jwt_extended import decode_token
from .user import User, UpdateProfilePic, UpdateInfo
from .post import Post, CreatePost, UpdatePost, DeletePost
from .comment import Comment, CreateComment, CreateReplyComment
from .claps import Clap, CreateClap
from .tags import Tags, CreateTag

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
    user = graphene.Field(User, uuid=graphene.Int())
    posts = graphene.List(Post)
    post = graphene.Field(Post, uuid=graphene.Int())
    comments = graphene.List(Comment)

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_posts(self, info):
        query = Post.get_query(info)
        return query.all()

    def resolve_comments(self, info):
        query = Comment.get_query(info)
        return query.all()

    def resolve_user(self, info , uuid):
        query = User.get_query(info)
        # token = info.context.headers.get('AUTHORIZATION')
        # token_type = decode_token(token)["type"]
        # email = None
        # if token_type == 'access':
        #     email = decode_token(token)['identity']
        # return query.filter_by(email=email).first()
        return query.get(uuid)

    def resolve_post(self, info, uuid):
        query = Post.get_query(info)
        return query.get(uuid)

schema = graphene.Schema(query=Query, mutation=Mutation, types=[User, Post])
