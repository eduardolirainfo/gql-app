from graphene import Argument, Int, List, ObjectType
from sqlalchemy.orm import joinedload

from gql_app.db.database import Session
from gql_app.db.models import Employer, Job
from gql_app.gql.types import EmployerObject, JobObject


class Query(ObjectType):
    employers = List(EmployerObject, id=Argument(Int))
    jobs = List(JobObject, employer_id=Argument(Int))

    @staticmethod
    def resolve_jobs(root, info, employer_id=None):
        # return Session().query(Job).all()
        session = Session()
        query = session.query(Job).options(joinedload(Job.employer))
        if employer_id is not None:
            query = query.filter(Job.employer_id == employer_id)
        return query.all()

    @staticmethod
    def resolve_employers(root, info, id=None):
        # return Session().query(Employer).all()
        session = Session()
        query = session.query(Employer).options(joinedload(Employer.jobs))
        if id is not None:
            query = query.filter(Employer.id == id)
        return query.all()
