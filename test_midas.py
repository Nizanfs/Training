import midas
import pytest
from datetime import datetime

from db_handler import use_session

terrorists = []
organizations = []
events = []


@pytest.fixture()
def fixture_session():
    yield from use_session()


@pytest.fixture()
def setup_test():
    midas.clear_all_tables()
    terrorists.extend([midas.add_terrorist('Hasan', 'Izz-Al-Din', 'Lebanon', 'Planner'),
                       midas.add_terrorist('Imad', 'Mughniyah', 'Damascus', 'Explosives Expert'),
                       midas.add_terrorist('Ibrahim', 'Salih Mohammed Al-Yacoub', 'USA', 'Weapons Expert'),
                       midas.add_terrorist('Osama', 'Bin Laden', 'Pakistan', 'Planner')])

    organizations.extend([midas.add_organization('Los Angeles', 'Al-Qaida'),
                          midas.add_organization('Chad', 'Boko Haram')])

    events.extend([midas.add_event('New York', datetime.now()),
                   midas.add_event('Tel Aviv', datetime.now())])

    midas.add_member_to_organization(terrorists[0], organizations[0])
    midas.add_member_to_organization(terrorists[1], organizations[0])
    midas.add_member_to_organization(terrorists[2], organizations[1])
    midas.add_member_to_organization(terrorists[3], organizations[1])

    midas.add_member_to_event(terrorists[0], events[0])
    midas.add_member_to_event(terrorists[0], events[1])
    midas.add_member_to_event(terrorists[1], events[0])
    midas.add_member_to_event(terrorists[2], events[0])
    midas.add_member_to_event(terrorists[3], events[1])


def test_fetching_terrorist(setup_test):
    new_terrorist = midas.add_terrorist('Hasan2', 'Izz-Al-Din2', 'Lebanon', 'Planner')
    terrorist = midas.get_terrorist(new_terrorist)
    assert terrorist is not None
    assert terrorist.name == new_terrorist.name
    assert terrorist.last_name == new_terrorist.last_name
    assert terrorist.role == new_terrorist.role
    assert terrorist.location == new_terrorist.location


def test_fetching_organization(setup_test):
    new_organization = midas.add_organization('London', 'Abu Sayyaf Group')
    organization = midas.get_organization(new_organization)
    assert organization is not None
    assert organization.name == new_organization.name
    assert organization.prime_location == new_organization.prime_location


def test_fetching_event(setup_test):
    new_event = midas.add_event('London', datetime.now())
    event = midas.get_event(new_event)
    assert event is not None
    assert event.location == new_event.location
    assert event.date == new_event.date


def test_organization_members(setup_test):
    organization = midas.get_organization(organizations[0])
    assert len(organization.members) == 2
    assert organization.members[0] == terrorists[0]
    assert organization.members[1] == terrorists[1]


def test_terrorist_organization(setup_test):
    terrorist = midas.get_terrorist(terrorists[0])
    assert terrorist.organization == organizations[0]


def test_event_participants(setup_test):
    event = midas.get_event(events[0])
    assert len(event.participants) == 3
    assert event.participants[0] == terrorists[0]
    assert event.participants[1] == terrorists[1]
    assert event.participants[2] == terrorists[2]
