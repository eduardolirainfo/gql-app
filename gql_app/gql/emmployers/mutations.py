import strawberry

from gql_app.db.database import Session
from gql_app.db.models import Employer
from gql_app.gql.emmployers.types import EmployerType


@strawberry.type
class AddEmployerPayload:
    employer: EmployerType


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_employer(
        self, name: str, email: str, industry: str
    ) -> AddEmployerPayload:
        employer = Employer(name=name, email=email, industry=industry)
        session = Session()
        session.add(employer)
        session.commit()
        session.refresh(employer)
        session.close()
        return AddEmployerPayload(employer=employer)
