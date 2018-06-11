from sqlalchemy import Column, Integer, VARCHAR, DateTime
from db_handler import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class OrganizationMember(Base):
    __tablename__ = 'organization_members'
    user_id = Column(Integer, ForeignKey('terrorists.id'), primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), primary_key=True)
    organization = relationship('Organization', backref=backref('organization_members'))
    member = relationship('Terrorist', uselist=False, backref=backref('organization_members'))

    def __repr__(self):
        return f'Event (user_id = {self.user_id}, organization_id = {self.organization_id})'
