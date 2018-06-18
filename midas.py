import db_handler
from terrorist import Terrorist
from organization import Organization
from event import Event
from sqlalchemy import desc, func


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
    """
    Persisting an entity to thje DB. Used as a base by all entity types
    :param session:
    :param entity:
    :return:
    """
    session.add(entity)
    session.commit()
    return entity


def get_entity_by_id(session, entity_id, entity_type):
    return session.query(entity_type).get(entity_id)


def add_member_to_organization(session, terrorist_id, organization_id):
    """
    Link a terrorist to an organization

    :param session:
    :param terrorist_id:
    :param organization_id:
    :return:
    """
    matched_organization = get_entity_by_id(session, organization_id, Organization)
    matched_terrorist = get_entity_by_id(session, terrorist_id, Terrorist)
    matched_organization.members.append(matched_terrorist)
    session.commit()


def add_member_to_event(session, terrorist_id, event_id):
    """
    Link a member to an event
    :param session:
    :param terrorist_id:
    :param event_id:
    :return:
    """
    matched_event = get_entity_by_id(session, event_id, Event)
    matched_terrorist = get_entity_by_id(session, terrorist_id, Terrorist)
    matched_event.participants.append(matched_terrorist)
    session.commit()


def get_members_not_kalab(session):
    """
    Get a list of members which are not stationed in the original location
    :param session:
    :return:
    """
    not_kalab_terrorists = session.query(Terrorist).join(Terrorist.organization)\
        .filter(Organization.prime_location != Terrorist.location)
    return [t.id for t in not_kalab_terrorists]


def get_last_event_participated_in(session):
    """
    Get a dictionary of terrorist and their last event participation date. in case there was None, None will be returned
    :param session:
    :return:
    """
    terrorist_ordered_events = session.query(Terrorist).join(Terrorist.events) \
        .order_by(desc(Event.date))
    result = {}
    for t in terrorist_ordered_events:
        last_event = t.events[0].date#max(t.date for t in t.events) if len(t.events) > 0 else None
        result[t.id] = last_event

    return result


def get_organizations_members_count(session):
    """
    Get a dictionary of all organization ids with the count of members for each
    :param session:
    :return:
    """
    organization_members_count = session.query(Organization, func.count(Terrorist.id))\
        .join(Organization.members).group_by(Organization.id)
    result = {}
    for o in organization_members_count:
        result[o[0].id] = o[1]
    return result


def get_organizations_count_per_event(session):
    """
    Get a dictionary of all organization ids with the count of events each participated in
    :param session:
    :return:
    """
    event_organizations_count = session.query(Event, func.count(Organization.id)) \
        .join(Event.participants).join(Terrorist.organization).group_by(Organization.id).group_by(Event.id)
    result = {}
    for o in event_organizations_count:
        result[o[0].id] = o[1]
    return result


def get_people_you_may_know(session):
    """
    Geta  dictionary of all terrorist ids with the related list of additional terrorists they might have encountered
    based on mutual events participated in
    :param session:
    :return:
    """
    events = session.query(Event).join(Event.participants).group_by(Event.id)
    result = {}
    for e in events:
        for t1 in e.participants:
            for t2 in e.participants:
                if t1.id == t2.id:
                    continue

                if t1.id not in result:
                    result[t1.id] = set()
                result[t1.id].add(t2.id)

    return result


db_handler.create_all_tables()
