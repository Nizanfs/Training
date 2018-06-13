from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, query, Query
from contextlib import contextmanager

Base = declarative_base()
engine = create_engine('sqlite:///midas.db', echo=True)
Session = sessionmaker(bind=engine)


def create_all_tables():
    Base.metadata.create_all(engine)


def recreate_all_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Refiner(Query):
    def __init__(self, entities, session=None):
        super().__init__(entities, session)

    def refine(self, *args, **kwargs):
        if len(kwargs) == 0:
            return self.filter(*args)
        return self.filter_by(**kwargs)


@contextmanager
def use_session():
    session = Session()
    yield session
    session.close()
