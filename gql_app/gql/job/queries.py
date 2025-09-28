from typing import List, Optional

import strawberry

from gql_app.db.database import Session
from gql_app.db.models import Job
from gql_app.gql.job.types import JobType


@strawberry.type
class Query:
    @strawberry.field
    def jobs(self, employer_id: Optional[int] = None) -> List[JobType]:
        session = Session()
        query = session.query(Job)
        if employer_id is not None:
            query = query.filter(Job.employer_id == employer_id)
        result = query.all()
        session.close()
        return result

    @strawberry.field
    def job(self, id: int) -> Optional[JobType]:
        session = Session()
        j = session.query(Job).filter(Job.id == id).first()
        session.close()
        return j
