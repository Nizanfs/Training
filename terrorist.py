from sqlalchemy import Column, Integer, VARCHAR
from db_handler import Base


class Terrorist(Base):
    __tablename__ = 'terrorists'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(30))
    last_name = Column(VARCHAR(30))
    role = Column(VARCHAR(256))
    location = Column(VARCHAR(256))

    def __repr__(self):
        return f'Terrorist (id = {self.id}, name = {self.name}, last_name={self.last_name}, role={self.role},' \
               f' location={self.location}'
