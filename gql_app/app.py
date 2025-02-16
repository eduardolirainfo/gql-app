import os

from dotenv import load_dotenv
from fastapi import FastAPI
from graphene import Field, Int, List, ObjectType, Schema, String
from sqlalchemy import Column, ForeignKey, Integer, create_engine
from sqlalchemy import String as saString
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from starlette_graphene3 import (
    GraphQLApp,
    make_graphiql_handler,
)

load_dotenv()

DB_URL = os.getenv('DB_URL')
engine = create_engine(DB_URL)
# conn = engine.connect()

Base = declarative_base()


class Employer(Base):
    __tablename__ = 'employers'

    id = Column(Integer, primary_key=True)
    name = Column(saString)
    email = Column(saString)
    industry = Column(saString)
    jobs = relationship('Job', back_populates='employer')


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(saString)
    description = Column(saString)
    employer_id = Column(Integer, ForeignKey('employers.id'))
    employer = relationship('Employer', back_populates='jobs')


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# emp1 = Employer(id=1, name='Apple', email='demo1@gmail.com', industry='Tech')
# session.add(emp1)


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
    {
        'id': 4,
        'name': 'Life Style',
        'email': 'demo4@gmail.com',
        'industry': 'Health',
    },
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
        'title': 'Psychologist',
        'description': 'Counselor',
        'employer_id': 3,
    },
    {
        'id': 4,
        'title': 'Software Engineer',
        'description': 'Java Developer',
        'employer_id': 4,
    },
    {
        'id': 5,
        'title': 'Plumber',
        'description': 'Indepedent Contractor',
        'employer_id': 2,
    },
]


def prepare_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
        emp_ = Employer(**employer)
        session.add(emp_)

    for job in jobs_data:
        job_ = Job(**job)
        session.add(job_)

    session.commit()
    session.close()


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
