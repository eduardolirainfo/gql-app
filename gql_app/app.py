import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from gql_app.db.database import Session, prepare_data
from gql_app.db.models import Employer, Job
from gql_app.gql.emmployers.mutations import Mutation as EmployerMutation
from gql_app.gql.emmployers.queries import Query as EmployerQuery
from gql_app.gql.job.mutations import Mutation as JobMutation
from gql_app.gql.job.queries import Query as JobQuery


@strawberry.type
class Mutation(EmployerMutation, JobMutation):
    pass


@strawberry.type
class Query(EmployerQuery, JobQuery):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    prepare_data()


graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix='/gql')


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
    session = Session()
    jobs = session.query(Job).all()
    session.close()
    return jobs


@app.get('/jobs/{job_id}')
def get_job(job_id: int):
    session = Session()
    job = session.query(Job).get(job_id)
    session.close()
    return job
