from fastapi import FastAPI
from graphene import Field, Int, List, ObjectType, Schema, String
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
)

employers_data = [
    {'id': 1, 'name': 'Apple', 'email': 'demo1@gmail.com', 'industry': 'Tech'},
    {
        'id': 2,
        'name': 'Money',
        'email': 'demo2@gmail.com',
        'industry': 'Finance',
    },
    {
        'id': 3,
        'name': 'Amazon',
        'email': 'demo3@gmail.com',
        'industry': 'Tech',
    },
    {'id': 4, 'name': 'Life', 'email': 'demo4@gmai.com', 'industry': 'Health'},
]

jobs_data = [
    {
        'id': 1,
        'title': 'Software Engineer',
        'description': 'Python Developer',
        'employer_id': 1,
    },
    {
        'id': 2,
        'title': 'Software Engineer',
        'description': 'JavaScript Developer',
        'employer_id': 2,
    },
    {
        'id': 3,
        'title': 'Software Engineer',
        'description': 'React Developer',
        'employer_id': 3,
    },
    {
        'id': 4,
        'title': 'Software Engineer',
        'description': 'Java Developer',
        'employer_id': 4,
    },
]


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return [job for job in jobs_data if job['employer_id'] == root['id']]


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        return next(
            employer
            for employer in employers_data
            if employer['id'] == root['employer_id']
        )


class Query(ObjectType):
    employers = List(EmployerObject)
    jobs = List(JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data

    @staticmethod
    def resolve_employers(root, info):
        return employers_data


schema = Schema(query=Query)

app = FastAPI()

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
