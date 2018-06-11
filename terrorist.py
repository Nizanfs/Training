from sqlalchemy import Column, Integer, VARCHAR
from db_handler import Base
from sqlalchemy.orm import relationship
from event_participant import EventParticipant
from organization_members import OrganizationMember


class Terrorist(Base):
    __tablename__ = 'terrorists'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(30))
    last_name = Column(VARCHAR(30))
    role = Column(VARCHAR(256))
    location = Column(VARCHAR(256))
    events = relationship('Event', secondary='event_participants')
    organization = relationship('Organization', uselist=False, secondary='organization_members')

    def __repr__(self):
        return f'Terrorist (id = {self.id}, name = {self.name}, last_name={self.last_name}, role={self.role},' \
               f' location={self.location})'
