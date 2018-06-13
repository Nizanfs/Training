import db_handler
from terrorist import Terrorist
from organization import Organization
from event import Event
from sqlalchemy import MetaData
meta = MetaData()


def add_terrorist(session, name, last_name, role, location):
    terrorist_instance = Terrorist(name=name, last_name=last_name, role=role, location=location)
    return add_entity(session, terrorist_instance)


def get_terrorist(session, entity_id):
    return get_entity_by_id(session, entity_id, Terrorist)


def add_organization(session, prime_location, name):
    organization_instance = Organization(prime_location=prime_location, name=name)
    return add_entity(session, organization_instance)


def get_organization(session, entity_id):
    return get_entity_by_id(session, entity_id, Organization)


def add_event(session, location, date):
    event_instance = Event(location=location, date=date)
    return add_entity(session, event_instance)


def get_event(session, entity_id):
    return get_entity_by_id(session, entity_id, Event)


def add_entity(session, entity):
    session.add(entity)
    session.commit()
    return entity


def get_entity_by_id(session, entity_id, entity_type):
    results = session.query(entity_type).filter(entity_type.id == entity_id)
    return results[0] if results.count() > 0 else None


def add_member_to_organization(session, terrorist_id, organization_id):
    matched_organization = get_entity_by_id(session, organization_id, Organization)
    matched_terrorist = get_entity_by_id(session, terrorist_id, Terrorist)
    matched_organization.members.append(matched_terrorist)
    session.commit()


def add_member_to_event(session, terrorist_id, event_id):
    matched_event = get_entity_by_id(session, event_id, Event)
    matched_terrorist = get_entity_by_id(session, terrorist_id, Terrorist)
    matched_event.participants.append(matched_terrorist)
    session.commit()


def get_members_not_kalab(session):
    all_terrorists = Terrorist.get(session).all()
    return [t.id for t in all_terrorists if not _is_member_kalab(t)]


def _is_member_kalab(terrorist):
    return terrorist.location == terrorist.organization.prime_location


def get_last_event_participated_in(session):
    all_terrorists = Terrorist.get(session).all()
    result = {}
    for t in all_terrorists:
        last_event = max(t.date for t in t.events) if len(t.events) > 0 else None
        result[t.id] = last_event

    return result


def get_organizations_members_count(session):
    all_organization = Organization.get(session).all()
    result = {}
    for o in all_organization:
        result[o.id] = len(o.members)

    return result


def get_organizations_count_per_event(session):
    all_events = Event.get(session).all()
    result = {}
    for e in all_events:
        organizations = set([t.organization.id for t in e.participants])
        result[e.id] = len(organizations)

    return result


def get_people_you_may_know(session):
    all_terrorists = Terrorist.get(session).all()
    result = {}
    for t in all_terrorists:
        possible_know = []
        result[t.id] = possible_know
        for t1 in all_terrorists:
            t_event_ids = set(e.id for e in t.events)
            t1_event_ids = set(e.id for e in t1.events)
            if t.id != t1.id and len(set.intersection(t_event_ids, t1_event_ids)) > 0:
                possible_know.append(t1.id)

    return result


db_handler.create_all_tables()
