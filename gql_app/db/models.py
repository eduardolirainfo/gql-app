from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from sqlalchemy import (
    String as saString,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Employer(Base):
    __tablename__ = 'employers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(saString)
    email = Column(saString)
    industry = Column(saString)
    jobs = relationship('Job', back_populates='employer', lazy='joined')


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(saString)
    description = Column(saString)
    employer_id = Column(Integer, ForeignKey('employers.id'))
    employer = relationship('Employer', back_populates='jobs', lazy='joined')
