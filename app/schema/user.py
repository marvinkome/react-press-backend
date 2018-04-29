import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql import GraphQLError
from flask_jwt_extended import get_jwt_identity

from ..model import User as UserModel
from .. import db

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

class UpdateProfilePic(graphene.Mutation):
    class Arguments:
        new_pic = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, new_pic):
        email = get_jwt_identity()
        if email is None:
            return GraphQLError('You need an access token to perform this action')

        user = UserModel.query.filter_by(email=email).first()
        if user is not None:
            user.gravatar_url = new_pic
            
        db.session.add(user)
        db.session.commit()
        return UpdateProfilePic(user=user)

class UpdateInfo(graphene.Mutation):
    class Arguments:
        new_full_name = graphene.String()
        new_description = graphene.String()

    user = graphene.Field(lambda: User)

    def mutate(self, info, new_full_name=None, new_description=None):
        email = get_jwt_identity()
        if email is None:
            return GraphQLError('You need an access token to perform this action')
            
        user = UserModel.query.filter_by(email=email).first()
        
        if user is not None:
            if new_full_name is not None:
                user.full_name = new_full_name
            if new_description is not None:
                user.description = new_description
            
        db.session.add(user)
        db.session.commit()
        return UpdateInfo(user=user)
