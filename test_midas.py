import midas
import pytest
from datetime import datetime

from db_handler import use_session, recreate_all_tables

terrorists = []
organizations = []
events = []


@pytest.fixture()
def session_setup():
    with use_session() as session:
        yield session


@pytest.fixture()
def db_session(session_setup):
    recreate_all_tables()
    terrorists.extend([midas.add_terrorist(session_setup, 'Hasan', 'Izz-Al-Din', 'Lebanon', 'Planner').id,
                       midas.add_terrorist(session_setup, 'Imad', 'Mughniyah', 'Damascus', 'Explosives Expert').id,
                       midas.add_terrorist(session_setup, 'Ibrahim', 'Salih Mohammed Al-Yacoub', 'USA', 'Weapons Expert').id,
                       midas.add_terrorist(session_setup, 'Osama', 'Bin Laden', 'Pakistan', 'Planner').id])

    organizations.extend([midas.add_organization(session_setup, 'Los Angeles', 'Al-Qaida').id,
                          midas.add_organization(session_setup, 'Chad', 'Boko Haram').id])

    events.extend([midas.add_event(session_setup, 'New York', datetime.now()).id,
                   midas.add_event(session_setup, 'Tel Aviv', datetime.now()).id])

    midas.add_member_to_organization(session_setup, terrorists[0], organizations[0])
    midas.add_member_to_organization(session_setup, terrorists[1], organizations[0])
    midas.add_member_to_organization(session_setup, terrorists[2], organizations[1])
    midas.add_member_to_organization(session_setup, terrorists[3], organizations[1])

    midas.add_member_to_event(session_setup, terrorists[0], events[0])
    midas.add_member_to_event(session_setup, terrorists[0], events[1])
    midas.add_member_to_event(session_setup, terrorists[1], events[0])
    midas.add_member_to_event(session_setup, terrorists[2], events[0])
    midas.add_member_to_event(session_setup, terrorists[3], events[1])
    return session_setup


def test_fetching_terrorist(db_session):
    new_terrorist = midas.add_terrorist(db_session, 'Hasan2', 'Izz-Al-Din2', 'Lebanon', 'Planner')
    terrorist = midas.get_terrorist(db_session, new_terrorist.id)
    assert terrorist is not None
    assert terrorist.name == new_terrorist.name
    assert terrorist.last_name == new_terrorist.last_name
    assert terrorist.role == new_terrorist.role
    assert terrorist.location == new_terrorist.location


def test_fetching_organization(db_session):
    new_organization = midas.add_organization(db_session, 'London', 'Abu Sayyaf Group')
    organization = midas.get_organization(db_session, new_organization.id)
    assert organization is not None
    assert organization.name == new_organization.name
    assert organization.prime_location == new_organization.prime_location


def test_fetching_event(db_session):
    new_event = midas.add_event(db_session, 'London', datetime.now())
    event = midas.get_event(db_session, new_event.id)
    assert event is not None
    assert event.location == new_event.location
    assert event.date == new_event.date


def test_organization_members(db_session):
    organization = midas.get_organization(db_session, organizations[0])
    assert len(organization.members) == 2
    assert organization.members[0].id == terrorists[0]
    assert organization.members[1].id == terrorists[1]


def test_terrorist_organization(db_session):
    terrorist = midas.get_terrorist(db_session, terrorists[0])
    assert terrorist.organization.id == organizations[0]


def test_event_participants(db_session):
    event = midas.get_event(db_session, events[0])
    assert len(event.participants) == 3
    assert event.participants[0].id == terrorists[0]
    assert event.participants[1].id == terrorists[1]
    assert event.participants[2].id == terrorists[2]
