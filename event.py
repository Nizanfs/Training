from sqlalchemy import Column, Integer, VARCHAR, DateTime
from db_handler import Base


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    location = Column(VARCHAR(256))
    date = Column(DateTime)

    def __repr__(self):
        return f'Event (id = {self.id}, location={self.location}, datetime = {self.date}'
