from sqlalchemy import Column, Integer, VARCHAR, DateTime
from db_handler import Base


class IpEntry(Base):
    __tablename__ = 'ips'
    id = Column(Integer, primary_key=True)
    ip = Column(VARCHAR(15))
    protocol = Column(VARCHAR(4))
    timestamp = Column(DateTime)

    def __repr__(self):
        return f'IpEntry (ip = {self.ip}, protocol={self.protocol}, timestamp={self.timestamp},'
