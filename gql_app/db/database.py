from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gql_app.db.data import employers_data, jobs_data
from gql_app.db.models import Base, Employer, Job
from gql_app.settings.config import DB_URL

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


def prepare_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
        emp_ = Employer(**employer)
        session.add(emp_)

    for job in jobs_data:
        job_ = Job(**job)
        session.add(job_)

    session.commit()
    session.close()
