from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
)

from gql_app.db.database import prepare_data
from gql_app.gql.queries import Query

schema = Schema(query=Query)

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    prepare_data()


app.mount(
    '/gql',
    GraphQLApp(schema=schema, on_get=make_graphiql_handler()),
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
