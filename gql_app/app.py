from fastapi import FastAPI
from graphene import ObjectType, Schema, String
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
    make_playground_handler,
)


class Query(ObjectType):
    hello = String(name=String(default_value='graphql'))

    def resolve_hello(root, info, name):
        return f'Hello {name}'


schema = Schema(query=Query)

app = FastAPI()
app.mount(
    '/gql',
    GraphQLApp(schema=schema, on_get=make_graphiql_handler()),
)

app.mount(
    '/gql-p',
    GraphQLApp(schema=schema, on_get=make_playground_handler()),
)

# @app.get('/')
# def read_root():
#     return {'Hello': 'World'}


# @app.get('/hello/{name}')
# def read_item(name: str):
#     return {'Hello': name}


# @app.get('/error')
# def read_error():
#     return JSONResponse(status_code=500, content={'error': 'Server error'})
