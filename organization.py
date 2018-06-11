from sqlalchemy import Column, Integer, VARCHAR
from db_handler import Base


class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    prime_location = Column(VARCHAR(256))
    name = Column(VARCHAR(30))

    def __repr__(self):
        return f'Organization (id = {self.id}, prime_location={self.prime_location}, name = {self.name}'
