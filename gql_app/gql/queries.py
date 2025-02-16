from graphene import List, ObjectType

from gql_app.db.data import employers_data, jobs_data
from gql_app.gql.types import EmployerObject, JobObject


class Query(ObjectType):
    employers = List(EmployerObject)
    jobs = List(JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data

    @staticmethod
    def resolve_employers(root, info):
        return employers_data
