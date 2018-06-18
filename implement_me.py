from db_handler import use_session
from ip_entry import IpEntry
from sqlalchemy import func, desc


def index(data):
    """
    Index the given entries.

    :note: May be called multiple times.

    :param data: A list of 'Entry' instances to index.
    """
    entries = [IpEntry(ip=e.ip, protocol=e.protocol, timestamp=e.timestamp) for e in data]

    with use_session() as session:
        session.bulk_save_objects(entries)
        session.commit()


def get_device_histogram(ip, n):
    """
    Return the latest 'n' entries for the given 'ip'.
    """
    with use_session() as session:
        results = session.query(IpEntry).filter(ip == ip).order_by(desc(IpEntry.timestamp)).limit(n)

    return [{'timestamp': ip.timestamp, 'protocol': ip.protocol} for ip in results]


def get_devices_status():
    """
    Return a list of every ip and the latest time it was seen it.
    """
    with use_session() as session:
        results = session.query(IpEntry, func.max(IpEntry.timestamp)).group_by(IpEntry.ip)

    return [(res.IpEntry.ip, res[1]) for res in results]
