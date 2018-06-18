from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from db_handler import Base, Refiner
from sqlalchemy.orm import relationship
from event_participant import EventParticipant


class Terrorist(Base):
    __tablename__ = 'terrorists'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(30))
    last_name = Column(VARCHAR(30))
    role = Column(VARCHAR(256))
    location = Column(VARCHAR(256))
    events = relationship('Event', secondary='event_participants', back_populates='participants')
    organization = relationship('Organization', back_populates='members')
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    @staticmethod
    def get(session):
        return Refiner(Terrorist, session)

    def __repr__(self):
        return f'Terrorist (name = {self.name}, last_name={self.last_name}, role={self.role},' \
               f' location={self.location})'
