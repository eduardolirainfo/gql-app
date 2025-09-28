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


# if __name__ == '__main__':
#     session = Session()
#     novo_employer = Employer(
#         name='Teste', email='teste@teste.com', industry='TI'
#     )
#     session.add(novo_employer)
#     session.commit()
#     session.refresh(novo_employer)
#     print(f'Employer inserido: {novo_employer.id}, {novo_employer.name}')

#     novo_job = Job(
#         title='Dev', description='Backend', employer_id=novo_employer.id
#     )
#     session.add(novo_job)
#     session.commit()
#     session.refresh(novo_job)
#     print(f'Job inserido: {novo_job.id}, {novo_job.title}')

#     employers = session.query(Employer).all()
#     jobs = session.query(Job).all()
#     print(f'Employers no banco: {[e.name for e in employers]}')
#     print(f'Jobs no banco: {[j.title for j in jobs]}')
#     session.close()
