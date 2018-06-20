from elasticsearch import Elasticsearch
from dateutil import parser
from elasticsearch.helpers import bulk

from redis_handler import get_redis_client
SEPARATOR = '-%$#'

redis = get_redis_client()


def clear_index():
    # redis.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    pass


def index(data):
    """
    Index the given entries.

    :note: May be called multiple times.

    :param data: A list of 'Entry' instances to index.
    """
    for entry in data:
        # value = f'{entry.timestamp}{SEPARATOR}{entry.protocol}'
        redis.zadd(entry.ip, entry.timestamp, entry.protocol)


def get_device_histogram(ip, n):
    """
    Return the latest 'n' entries for the given 'ip'.
    """
    result = []
    for entry in redis.zrange(ip, 0, n-1):
        values = entry.split(SEPARATOR)
        result.append({'timestamp': parser.parse(values[0]), 'protocol': values[1]})

    return result


def get_devices_status():
    """
    Return a list of every ip and the latest time it was seen it.
    """
    ip_grouping_key = 'ip_grouping'
    latest_timestamp_key = 'latest_timestamp_key'
    get_ips_latest_timestamp = {
        'size': 0,
        'aggs': {
            ip_grouping_key: {
                'terms': {
                    'size': MAX_DOCUMENTS,
                    'field': 'ip'
                },
                'aggs': {
                    latest_timestamp_key: {
                        'max': {
                            'field': 'timestamp'
                        }
                    }
                }
            }
        }
    }

    redis.indices.refresh(index=INDEX_NAME)
    res = redis.search(INDEX_NAME, ENTRY_TYPE, get_ips_latest_timestamp)
    buckets = res['aggregations'][ip_grouping_key]['buckets']

    return [(ip['key'], parser.parse(ip[latest_timestamp_key]['value_as_string'], ignoretz=True)) for ip in buckets]