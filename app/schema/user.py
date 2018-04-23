import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..model import User as UserModel
from .. import db

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )

class UpdateProfilePic(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        new_pic = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, new_pic, user_id):
        user = UserModel.query.filter_by(uuid=user_id).first()
        if user is not None:
            user.gravatar_url = new_pic
            
        db.session.add(user)
        db.session.commit()
        return UpdateProfilePic(user=user)

class UpdateInfo(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        new_full_name = graphene.String()
        new_description = graphene.String()

    user = graphene.Field(lambda: User)

    def mutate(self, info, user_id, new_full_name=None, new_description=None):
        user = UserModel.query.filter_by(uuid=user_id).first()
        if user is not None:
            if new_full_name is not None:
                user.full_name = new_full_name
            if new_description is not None:
                user.description = new_description
            
        db.session.add(user)
        db.session.commit()
        return UpdateInfo(user=user)
