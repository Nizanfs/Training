from sqlalchemy import Column, Integer, VARCHAR, DateTime
from db_handler import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class EventParticipant(Base):
    __tablename__ = 'event_participants'
    user_id = Column(Integer, ForeignKey('terrorists.id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)

    def __repr__(self):
        return f'Event (user_id = {self.user_id}, event_id = {self.event_id})'
