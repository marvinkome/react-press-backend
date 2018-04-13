# from flask import 
from . import main
from flask_graphql import GraphQLView

# main.add_url_rule(
#     '/graphql',
#     view_func=GraphQLView.as_view(
#         'graphql',
#         schema=schema,
#         graphiql=True # for having the GraphiQL interface
#     )
# )

@main.route('/')
def hello():
    return '<p>HEllo world</p>'