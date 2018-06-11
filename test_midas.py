import midas
from datetime import datetime


def test_adding_terrorist():
    new_terrorist = midas.add_terrorist('a', 'b', 'c', 'd')
    terrorist = midas.get_terrorist(new_terrorist.id)
    assert terrorist is not None
    assert terrorist.name == new_terrorist.name
    assert terrorist.last_name == new_terrorist.last_name
    assert terrorist.role == new_terrorist.role
    assert terrorist.location == new_terrorist.location


def test_adding_organization():
    new_organization = midas.add_organization('Los Angeles', 'Al-Qaida')
    organization = midas.get_organization(new_organization.id)
    assert organization is not None
    assert organization.name == new_organization.name
    assert organization.prime_location == new_organization.prime_location


def test_adding_event():
    new_event = midas.add_event('New York', datetime.now())
    event = midas.get_event(new_event.id)
    assert event is not None
    assert event.location == new_event.location
    assert event.date == new_event.date

