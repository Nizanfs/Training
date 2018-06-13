import midas
import pytest
from datetime import datetime, timedelta
from db_handler import use_session, recreate_all_tables
from terrorist import Terrorist

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
                       midas.add_terrorist(session_setup, 'Ibrahim', 'Salih Mohammed Al-Yacoub', 'Weapons Expert', 'USA'
                                           ).id,
                       midas.add_terrorist(session_setup, 'Osama', 'Bin Laden', 'Planner', 'Africa').id,
                       midas.add_terrorist(session_setup, 'Ahmed', 'Bin Iber', 'Explosives Expert', 'USA').id,
                       midas.add_terrorist(session_setup, 'Yusuf', 'Akber', 'Decoy', 'Jordan').id])

    events.extend([midas.add_event(session_setup, 'New York', datetime.now() + timedelta(days=-30)).id,
                   midas.add_event(session_setup, 'Tel Aviv', datetime.now()).id,
                   midas.add_event(session_setup, 'Bangladesh', datetime.now() + timedelta(days=-3)).id,
                   midas.add_event(session_setup, 'London', datetime.now()).id])

    midas.add_member_to_organization(session_setup, terrorists[0], organizations[0])
    midas.add_member_to_organization(session_setup, terrorists[1], organizations[0])
    midas.add_member_to_organization(session_setup, terrorists[2], organizations[1])
    midas.add_member_to_organization(session_setup, terrorists[3], organizations[1])
    midas.add_member_to_organization(session_setup, terrorists[4], organizations[0])
    midas.add_member_to_organization(session_setup, terrorists[5], organizations[0])

    midas.add_member_to_event(session_setup, terrorists[0], events[0])
    midas.add_member_to_event(session_setup, terrorists[0], events[1])
    midas.add_member_to_event(session_setup, terrorists[1], events[0])
    midas.add_member_to_event(session_setup, terrorists[2], events[0])
    midas.add_member_to_event(session_setup, terrorists[3], events[1])
    midas.add_member_to_event(session_setup, terrorists[3], events[1])
    midas.add_member_to_event(session_setup, terrorists[0], events[2])
    midas.add_member_to_event(session_setup, terrorists[1], events[3])
    midas.add_member_to_event(session_setup, terrorists[5], events[3])
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
    assert len(organization.members) == 4
    assert organization.members[0].id == terrorists[0]
    assert organization.members[1].id == terrorists[1]
    assert organization.members[2].id == terrorists[4]
    assert organization.members[3].id == terrorists[5]


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
    actual_not_kalab = {1, 2, 3, 6}
    assert len(not_kalab) == len(actual_not_kalab)
    assert len(set.intersection(set(not_kalab), actual_not_kalab)) == len(actual_not_kalab)


def test_last_event_participated_in(db_session):
    terrorist_last_event_date = midas.get_last_event_participated_in(db_session)
    assert len(terrorist_last_event_date) == len(terrorists)
    assert terrorist_last_event_date[terrorists[4]] is None
    event_date = midas.get_event(db_session, events[1]).date
    assert terrorist_last_event_date[terrorists[0]] == event_date


def test_get_organizations_members_count(db_session):
    organization_members_count = midas.get_organizations_members_count(db_session)
    assert len(organization_members_count) == len(organizations)
    assert organization_members_count[organizations[0]] == 4
    assert organization_members_count[organizations[1]] == 2


def test_get_organizations_count_per_event(db_session):
    organization_count_per_event = midas.get_organizations_count_per_event(db_session)
    assert len(organization_count_per_event) == len(events)
    assert organization_count_per_event[events[0]] == 2
    assert organization_count_per_event[events[1]] == 2
    assert organization_count_per_event[events[2]] == 1
    assert organization_count_per_event[events[3]] == 1


def test_people_you_may_know(db_session):
    people_you_may_know = midas.get_people_you_may_know(db_session)
    assert len(people_you_may_know) == len(terrorists)
    assert len(people_you_may_know[terrorists[0]]) == 3
    assert len(people_you_may_know[terrorists[1]]) == 3
    assert len(people_you_may_know[terrorists[2]]) == 2
    assert len(people_you_may_know[terrorists[3]]) == 1
    assert len(people_you_may_know[terrorists[4]]) == 0
    assert len(people_you_may_know[terrorists[5]]) == 1


def test_refine_functionality(db_session):
    terrorist_name = 'Osama'
    single_terrorist = list(Terrorist.get(db_session).refine(name=terrorist_name))
    single_terrorist2 = list(Terrorist.get(db_session).refine(Terrorist.name == terrorist_name))
    assert len(single_terrorist) == 1
    assert single_terrorist[0].name == terrorist_name

    assert len(single_terrorist2) == 1
    assert single_terrorist2[0].name == terrorist_name

    actual_usa_terrorists = ['Ibrahim', 'Ahmed']
    usa_terrorists = Terrorist.get(db_session).refine(location='USA')
    usa_terrorists_list = list(usa_terrorists)
    assert len(usa_terrorists_list) == 2
    assert usa_terrorists_list[0].name == actual_usa_terrorists[0]

    ordered_terrorists = list(usa_terrorists.order_by(Terrorist.name))
    assert len(ordered_terrorists) == 2
    assert ordered_terrorists[0].name == actual_usa_terrorists[1]
    single_terrorist_usa = usa_terrorists.first()
    assert single_terrorist_usa.name == actual_usa_terrorists[0]
