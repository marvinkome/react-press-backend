# from flask import 
from . import main
from flask_graphql import GraphQLView
from .. import db
from ..schema import schema

main.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)
