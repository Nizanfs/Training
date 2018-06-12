import midas
import pytest
from datetime import datetime, timedelta

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
    terrorists.clear()
    organizations.clear()
    events.clear()

    organizations.extend([midas.add_organization(session_setup, 'USA', 'Al-Qaida').id,
                          midas.add_organization(session_setup, 'Africa', 'Boko Haram').id])

    terrorists.extend([midas.add_terrorist(session_setup, 'Hasan', 'Izz-Al-Din', 'Planner', 'Lebanon').id,
                       midas.add_terrorist(session_setup, 'Imad', 'Mughniyah', 'Explosives Expert', 'Damascus').id,
                       midas.add_terrorist(session_setup, 'Ibrahim', 'Salih Mohammed Al-Yacoub', 'Weapons Expert', 'USA').id,
                       midas.add_terrorist(session_setup, 'Osama', 'Bin Laden', 'Planner', 'Africa').id,
                       midas.add_terrorist(session_setup, 'Ahmed', 'Bin Iber', 'Explosives Expert', 'USA').id])

    events.extend([midas.add_event(session_setup, 'New York', datetime.now() + timedelta(days=-30)).id,
                   midas.add_event(session_setup, 'Tel Aviv', datetime.now()).id,
                   midas.add_event(session_setup, 'Bangladesh', datetime.now() + timedelta(days=-3)).id,
                   midas.add_event(session_setup, 'London', datetime.now()).id])

    midas.add_member_to_organization(session_setup, terrorists[0], organizations[0])
    midas.add_member_to_organization(session_setup, terrorists[1], organizations[0])
    midas.add_member_to_organization(session_setup, terrorists[2], organizations[1])
    midas.add_member_to_organization(session_setup, terrorists[3], organizations[1])
    midas.add_member_to_organization(session_setup, terrorists[4], organizations[0])

    midas.add_member_to_event(session_setup, terrorists[0], events[0])
    midas.add_member_to_event(session_setup, terrorists[0], events[1])
    midas.add_member_to_event(session_setup, terrorists[1], events[0])
    midas.add_member_to_event(session_setup, terrorists[2], events[0])
    midas.add_member_to_event(session_setup, terrorists[3], events[1])
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
    assert len(organization.members) == 3
    assert organization.members[0].id == terrorists[0]
    assert organization.members[1].id == terrorists[1]
    assert organization.members[2].id == terrorists[4]


def test_terrorist_organization(db_session):
    terrorist = midas.get_terrorist(db_session, terrorists[0])
    assert terrorist.organization.id == organizations[0]


def test_event_participants(db_session):
    event = midas.get_event(db_session, events[0])
    assert len(event.participants) == 3
    assert event.participants[0].id == terrorists[0]
    assert event.participants[1].id == terrorists[1]
    assert event.participants[2].id == terrorists[2]


def test_get_members_not_kalab(db_session):
    not_kalab = midas.get_members_not_kalab(db_session)
    assert len(not_kalab) == 3
    assert len(set.intersection(set(not_kalab), set([1, 2, 3]))) == 3


def test_last_event_participated_in(db_session):
    terrorist_last_event_date = midas.get_last_event_participated_in(db_session)
    assert len(terrorist_last_event_date) == len(terrorists)
    assert terrorist_last_event_date[terrorists[4]] is None
    event_date = midas.get_event(db_session, events[1]).date
    assert terrorist_last_event_date[terrorists[0]] == event_date
    # assert len(set.intersection(set(terrorist_last_event_date), set([1, 2, 3]))) == 3
