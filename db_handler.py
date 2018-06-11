from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


Base = declarative_base()
engine = create_engine('sqlite:///midas.db', echo=True)
Session = sessionmaker(bind=engine)


def create_all_tables():
    Base.metadata.create_all(engine)


@contextmanager
def use_session():
    session = Session()
    yield session
