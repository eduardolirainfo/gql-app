from graphene import Argument, Field, Int, List, ObjectType

from gql_app.db.database import Session
from gql_app.db.models import Employer, Job
from gql_app.gql.types import EmployerObject, JobObject


class Query(ObjectType):
    employers = List(EmployerObject, id=Argument(Int))
    job = Field(JobObject, id=Int(required=True))
    jobs = List(JobObject, employer_id=Argument(Int))

    @staticmethod
    def resolve_job(root, info, id):
        # session = Session()
        # job = session.query(Job).filter(Job.id == id).first()
        # if job is None:
        #     raise ValueError(f"Job with id {id} not found")
        # session.close()
        return Session().query(Job).filter(Job.id == id).first()

    @staticmethod
    def resolve_jobs(root, info, employer_id=None):
        # return Session().query(Job).all()
        session = Session()
        query = session.query(Job)
        if employer_id is not None:
            query = query.filter(Job.employer_id == employer_id)
        return query.all()

    @staticmethod
    def resolve_employers(root, info, id=None):
        # return Session().query(Employer).all()
        session = Session()
        query = session.query(Employer)
        if id is not None:
            query = query.filter(Employer.id == id)
        return query.all()
