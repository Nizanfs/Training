from sqlalchemy import Column, Integer, VARCHAR
from db_handler import Base, Refiner
from sqlalchemy.orm import relationship


class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    prime_location = Column(VARCHAR(256))
    name = Column(VARCHAR(30))
    members = relationship('Terrorist', secondary='organization_members')

    @staticmethod
    def get(session):
        return Refiner(Organization, session)

    def __repr__(self):
        return f'Organization (id = {self.id}, prime_location={self.prime_location}, name = {self.name})'
