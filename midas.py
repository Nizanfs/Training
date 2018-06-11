import db_handler
import terrorist
import organization
import event


def add_terrorist(name, last_name, role, location):
    terrorist_instance = terrorist.Terrorist(name=name, last_name=last_name, role=role, location=location)
    return add_entity(terrorist_instance)


def get_terrorist(entity_id):
    return get_entity_by_id(entity_id, terrorist.Terrorist)


def add_organization(prime_location, name):
    organization_instance = organization.Organization(prime_location=prime_location, name=name)
    return add_entity(organization_instance)


def get_organization(entity_id):
    return get_entity_by_id(entity_id, organization.Organization)


def add_event(location, date):
    event_instance = event.Event(location=location, date=date)
    return add_entity(event_instance)


def get_event(entity_id):
    return get_entity_by_id(entity_id, event.Event)


def add_entity(entity):
    with db_handler.use_session() as session:
        session.add(entity)
        session.commit()
    return entity


def get_entity_by_id(entity_id, entity_type):
    with db_handler.use_session() as session:
        results = session.query(entity_type).filter(entity_type.id == entity_id)

    return results[0] if results.count() > 0 else None


def add_member_to_organization(terrorist_id, organization_id):
    matched_organization = get_organization(organization_id)
    matched_terrorist = get_terrorist(terrorist_id)
    with db_handler.use_session() as session:
        matched_organization.members.append(matched_terrorist)
        session.commit()


def add_member_to_event(terrorist_id, event_id):
    matched_event = get_event(event_id)
    matched_terrorist = get_terrorist(terrorist_id)
    with db_handler.use_session() as session:
        matched_event.participants.append(matched_terrorist)
        session.commit()


db_handler.create_all_tables()
