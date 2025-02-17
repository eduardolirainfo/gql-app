from graphene import Field, Int, Mutation, ObjectType, String

from gql_app.db.database import Session
from gql_app.db.models import Job
from gql_app.gql.types import JobObject


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        job = Job(
            title=title,
            description=description,
            employer_id=employer_id,
        )
        session = Session()
        session.add(job)
        session.commit()
        session.refresh(job)
        return AddJob(job=job)


class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(
        root, info, job_id, title=None, description=None, employer_id=None
    ):
        session = Session()
        job = session.query(Job).filter(Job.id == job_id).first()

        if not job:
            raise Exception(f'Job with id {id} not found')

        if title:
            job.title = title
        if description:
            job.description = description
        if employer_id:
            job.employer_id = employer_id

        session.commit()
        session.refresh(job)
        session.close()
        return UpdateJob(job=job)


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
