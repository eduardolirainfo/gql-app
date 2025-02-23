from graphene import Boolean, Field, Int, Mutation, ObjectType, String

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
    def mutate(root, info, job_id, **kwargs):
        session = Session()
        job = session.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise Exception(f'Job com id {job_id} não encontrado')

        for key, value in kwargs.items():
            setattr(job, key, value)

        session.commit()
        session.refresh(job)
        session.close()
        return UpdateJob(job=job)


class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    def mutate(root, info, id):
        session = Session()
        job = session.query(Job).filter(Job.id == id).first()
        if not job:
            raise Exception(f'Job com id {id} não encontrado')

        session.delete(job)
        session.commit()
        session.close()
        return DeleteJob(success=True)


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
