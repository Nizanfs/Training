from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

Base = declarative_base()
engine = create_engine('sqlite:///game_of_dbs.db', echo=True)
Session = sessionmaker(bind=engine)


def create_all_tables():
    Base.metadata.create_all(engine)


def recreate_all_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@contextmanager
def use_session():
    session = Session()
    yield session
    session.close()
