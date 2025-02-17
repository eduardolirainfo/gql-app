from graphene import List, ObjectType
from sqlalchemy.orm import joinedload

from gql_app.db.database import Session
from gql_app.db.models import Employer, Job
from gql_app.gql.types import EmployerObject, JobObject


class Query(ObjectType):
    employers = List(EmployerObject)
    jobs = List(JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        # return Session().query(Job).all()
        return Session().query(Job).options(joinedload(Job.employer)).all()

    @staticmethod
    def resolve_employers(root, info):
        # return Session().query(Employer).all()
        return (
            Session().query(Employer).options(joinedload(Employer.jobs)).all()
        )
