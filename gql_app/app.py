from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
)

from gql_app.db.database import Session, prepare_data
from gql_app.db.models import Employer, Job
from gql_app.gql.mutations import Mutation
from gql_app.gql.queries import Query

schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    prepare_data()


app.mount(
    '/gql',
    GraphQLApp(schema=schema, on_get=make_graphiql_handler()),
)


@app.get('/employers')
def get_employers():
    session = Session()
    employers = session.query(Employer).all()
    session.close()
    return employers


@app.get('/employers/{employer_id}')
def get_employer(employer_id: int):
    session = Session()
    employer = session.query(Employer).get(employer_id)
    session.close()
    return employer


@app.get('/jobs')
def get_jobs():
    with Session() as session:
        jobs = session.query(Job).all()
        return jobs


@app.get('/jobs/{job_id}')
def get_job(job_id: int):
    with Session() as session:
        job = session.query(Job).get(job_id)
        return job
