import midas
import pytest
from datetime import datetime


class TestMidas(object):
    terrorists = []
    organizations = []
    events = []

    def setup_class(self):
        self.terrorists.extend([midas.add_terrorist('Hasan', 'Izz-Al-Din', 'Lebanon', 'Planner').id,
                                midas.add_terrorist('Imad', 'Mughniyah', 'Damascus', 'Explosives Expert').id,
                                midas.add_terrorist('Ibrahim', 'Salih Mohammed Al-Yacoub', 'USA', 'Weapons Expert').id,
                                midas.add_terrorist('Osama', 'Bin Laden', 'Pakistan', 'Planner').id])

        self.organizations.extend([midas.add_organization('Los Angeles', 'Al-Qaida').id,
                                   midas.add_organization('Chad', 'Boko Haram').id])

        self.events.extend([midas.add_event('New York', datetime.now()).id,
                            midas.add_event('Tel Aviv', datetime.now()).id])

        midas.add_member_to_organization(self.terrorists[0], self.organizations[0])
        midas.add_member_to_organization(self.terrorists[1], self.organizations[0])
        midas.add_member_to_organization(self.terrorists[2], self.organizations[1])
        midas.add_member_to_organization(self.terrorists[3], self.organizations[1])

        midas.add_member_to_event(self.terrorists[0], self.events[0])
        midas.add_member_to_event(self.terrorists[0], self.events[1])
        midas.add_member_to_event(self.terrorists[1], self.events[0])
        midas.add_member_to_event(self.terrorists[2], self.events[0])
        midas.add_member_to_event(self.terrorists[3], self.events[1])

    def test_fetching_terrorist(self):
        new_terrorist = midas.add_terrorist('Hasan2', 'Izz-Al-Din2', 'Lebanon', 'Planner')
        terrorist = midas.get_terrorist(new_terrorist.id)
        assert terrorist is not None
        assert terrorist.name == new_terrorist.name
        assert terrorist.last_name == new_terrorist.last_name
        assert terrorist.role == new_terrorist.role
        assert terrorist.location == new_terrorist.location

    def test_fetching_organization(self):
        new_organization = midas.add_organization('London', 'Abu Sayyaf Group')
        organization = midas.get_organization(new_organization.id)
        assert organization is not None
        assert organization.name == new_organization.name
        assert organization.prime_location == new_organization.prime_location

    def test_fetching_event(self):
        new_event = midas.add_event('London', datetime.now())
        event = midas.get_event(new_event.id)
        assert event is not None
        assert event.location == new_event.location
        assert event.date == new_event.date

    def test_organization_members(self):
        organization = midas.get_organization(self.organizations[0])
        assert len(organization.members) == 2
        assert organization.members[0].id == self.terrorists[0]
        assert organization.members[1].id == self.terrorists[1]

    def test_terrorist_organization(self):
        terrorist = midas.get_terrorist(self.terrorists[0])
        assert terrorist.organization.id == self.organizations[0]

    def test_event_participants(self):
        event = midas.get_event(self.events[0])
        assert len(event.participants) == 3
        assert event.participants[0].id == self.terrorists[0]
        assert event.participants[1].id == self.terrorists[1]
        assert event.participants[2].id == self.terrorists[2]
