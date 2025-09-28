from typing import List

import strawberry

JobType = strawberry.LazyType('JobType', 'gql_app.gql.job.types')


@strawberry.type
class EmployerType:
    id: int
    name: str
    email: str
    industry: str

    @strawberry.field
    def jobs(self) -> List[JobType]:  # type: ignore
        return self.jobs
