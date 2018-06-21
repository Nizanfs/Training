from dateutil import parser as date_parser

from redis_handler import get_redis_client
SEPARATOR = '-%$#'

redis = get_redis_client()


def clear_index():
    pass


def index(data):
    """
    Index the given entries.

    :note: May be called multiple times.

    :param data: A list of 'Entry' instances to index.
    """
    for entry in data:
        value = f'{entry.timestamp}{SEPARATOR}{entry.protocol}'
        redis.zadd(entry.ip, entry.timestamp.timestamp(), value)


def get_device_histogram(ip, n):
    """
    Return the latest 'n' entries for the given 'ip'.
    """
    result = []
    for entry in redis.zrevrange(ip, 0, n-1):
        values = str(entry.decode()).split(SEPARATOR)
        result.append({'timestamp': date_parser.parse(values[0]), 'protocol': values[1]})

    return result


def get_devices_status():
    """
    Return a list of every ip and the latest time it was seen it.
    """
    result = []
    for key in redis.keys():
        ip = key.decode()
        entry = redis.zrevrange(ip, 0, 0)[0]
        values = str(entry.decode()).split(SEPARATOR)
        result.append((ip, date_parser.parse(values[0])))

    return result
