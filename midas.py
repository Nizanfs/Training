import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

def add_terrorist(id, name, last_name, role, location):
    pass


class Terrorist(Base):
    __tablename__ = 'terrorists'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(30))
    
