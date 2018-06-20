import datetime as dt
from datetime import datetime
from elasticsearch import Elasticsearch
from dateutil import parser
from elasticsearch.helpers import bulk

INDEX_NAME = 'entry-index'
ENTRY_TYPE = 'ip_entry'
MAX_DOCUMENTS = 100000
BULK_SIZE = 1000

es = Elasticsearch(f'http://localhost:9200')


def clear_index():
    es.indices.delete(index=INDEX_NAME)
    init_mapping()


def init_mapping():
    index_mapping = """{
        "mappings": {
            "ip_entry":
                {
                  "properties": {
                    "ip": { 
                      "type":     "text",
                      "fielddata": true
                    }
                  }
                }
        }
    }"""
    if not es.indices.exists(INDEX_NAME):
        es.indices.create(INDEX_NAME, index_mapping)

    mapping = es.indices.get(INDEX_NAME)[INDEX_NAME]['mappings'][ENTRY_TYPE]

def index(data):
    """
    Index the given entries.

    :note: May be called multiple times.

    :param data: A list of 'Entry' instances to index.
    """
    indexes = []
    for entry in data:
        doc = dict(entry._asdict())
        doc['_type'] = ENTRY_TYPE
        doc['_index'] = INDEX_NAME
        indexes.append(doc)
        # Index in bulks.
        if len(indexes) == BULK_SIZE:
            bulk(es, indexes)
            indexes.clear()

    bulk(es, indexes)
    es.indices.flush()


def get_device_histogram(ip, n):
    """
    Return the latest 'n' entries for the given 'ip'.
    """
    query = {
        'match': {'ip': ip}
    }

    body = {
        'from': 0,
        'size': n,
        'sort': {
            'timestamp': {
                'order': 'desc'
            }
        },
        'query': query

    }
    es.indices.refresh(index=INDEX_NAME)

    res = es.search(INDEX_NAME, ENTRY_TYPE, body)
    hits = res['hits']['hits']
    return [{'timestamp': parser.parse(ip['_source']['timestamp']), 'protocol': ip['_source']['protocol']}
            for ip in hits]


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

    es.indices.refresh(index=INDEX_NAME)
    res = es.search(INDEX_NAME, ENTRY_TYPE, get_ips_latest_timestamp)
    buckets = res['aggregations'][ip_grouping_key]['buckets']

    return [(ip['key'], parser.parse(ip[latest_timestamp_key]['value_as_string'], ignoretz=True)) for ip in buckets]