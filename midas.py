import db_handler
import terrorist
import organization
import event
from sqlalchemy import MetaData
meta = MetaData()


def add_terrorist(session, name, last_name, role, location):
    terrorist_instance = terrorist.Terrorist(name=name, last_name=last_name, role=role, location=location)
    return add_entity(session, terrorist_instance)


def get_terrorist(session, entity_id):
    return get_entity_by_id(session, entity_id, terrorist.Terrorist)


def add_organization(session, prime_location, name):
    organization_instance = organization.Organization(prime_location=prime_location, name=name)
    return add_entity(session, organization_instance)


def get_organization(session, entity_id):
    return get_entity_by_id(session, entity_id, organization.Organization)


def add_event(session, location, date):
    event_instance = event.Event(location=location, date=date)
    return add_entity(session, event_instance)


def get_event(session, entity_id):
    return get_entity_by_id(session, entity_id, event.Event)


def add_entity(session, entity):
    session.add(entity)
    session.commit()
    return entity


def get_entity_by_id(session, entity_id, entity_type):
    results = session.query(entity_type).filter(entity_type.id == entity_id)
    return results[0] if results.count() > 0 else None


def add_member_to_organization(session, terrorist_id, organization_id):
    matched_organization = get_entity_by_id(session, organization_id, organization.Organization)
    matched_terrorist = get_entity_by_id(session, terrorist_id, terrorist.Terrorist)
    matched_organization.members.append(matched_terrorist)
    session.commit()


def add_member_to_event(session, terrorist_id, event_id):
    matched_event = get_entity_by_id(session, event_id, event.Event)
    matched_terrorist = get_entity_by_id(session, terrorist_id, terrorist.Terrorist)
    matched_event.participants.append(matched_terrorist)
    session.commit()


db_handler.create_all_tables()
