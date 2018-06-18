from sqlalchemy import Column, Integer, VARCHAR, DateTime
from db_handler import Base, Refiner
from sqlalchemy.orm import relationship


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    location = Column(VARCHAR(256))
    date = Column(DateTime)
    participants = relationship('Terrorist', secondary='event_participants', back_populates='events')

    @staticmethod
    def get(session):
        return Refiner(Event, session)

    def __repr__(self):
        return f'Event (location={self.location}, date = {self.date})'
