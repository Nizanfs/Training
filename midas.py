import db_handler
import terrorist


def add_terrorist(name, last_name, role, location):
    terrorist_instance = terrorist.Terrorist(name=name, last_name=last_name, role=role, location=location)
    with db_handler.use_session() as session:
        session.add(terrorist_instance)
        session.commit()
    return terrorist_instance


def get_terrorist(id):
    with db_handler.use_session() as session:
        results = session.query(terrorist.Terrorist).filter(terrorist.Terrorist.id == id)

    return results[0] if results.count() > 0 else None


db_handler.create_all_tables()
