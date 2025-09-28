from typing import List, Optional

import strawberry

from gql_app.db.database import Session
from gql_app.db.models import Employer
from gql_app.gql.emmployers.types import EmployerType


@strawberry.type
class Query:
    @strawberry.field
    def employers(self, id: Optional[int] = None) -> List[EmployerType]:
        session = Session()
        query = session.query(Employer)
        if id is not None:
            query = query.filter(Employer.id == id)
        result = query.all()
        session.close()
        return result

    @strawberry.field
    def employer(self, id: int) -> Optional[EmployerType]:
        session = Session()
        emp = session.query(Employer).filter(Employer.id == id).first()
        session.close()
        return emp
