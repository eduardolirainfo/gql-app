from typing import Optional

import strawberry

EmployerType = strawberry.LazyType(
    'EmployerType', 'gql_app.gql.emmployers.types'
)


@strawberry.type
class JobType:
    id: int
    title: str
    description: str
    employer_id: int

    @strawberry.field
    def employer(self) -> Optional['EmployerType']:  # type: ignore
        return self.employer
