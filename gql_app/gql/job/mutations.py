from typing import Optional

import strawberry

from gql_app.db.database import Session
from gql_app.db.models import Job
from gql_app.gql.job.types import JobType


@strawberry.type
class AddJobPayload:
    job: JobType


@strawberry.type
class UpdateJobPayload:
    job: JobType


@strawberry.type
class DeleteJobPayload:
    success: bool


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_job(
        self, title: str, description: str, employer_id: int
    ) -> AddJobPayload:
        job = Job(
            title=title, description=description, employer_id=employer_id
        )
        session = Session()
        session.add(job)
        session.commit()
        session.refresh(job)
        session.close()
        return AddJobPayload(job=job)

    @strawberry.mutation
    def update_job(
        self,
        job_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        employer_id: Optional[int] = None,
    ) -> UpdateJobPayload:
        session = Session()
        job = session.query(Job).filter(Job.id == job_id).first()
        if not job:
            session.close()
            raise Exception(f'Job com id {job_id} não encontrado')
        if title is not None:
            job.title = title
        if description is not None:
            job.description = description
        if employer_id is not None:
            job.employer_id = employer_id
        session.commit()
        session.refresh(job)
        session.close()
        return UpdateJobPayload(job=job)

    @strawberry.mutation
    def delete_job(self, id: int) -> DeleteJobPayload:
        session = Session()
        job = session.query(Job).filter(Job.id == id).first()
        if not job:
            session.close()
            raise Exception(f'Job com id {id} não encontrado')
        session.delete(job)
        session.commit()
        session.close()
        return DeleteJobPayload(success=True)
