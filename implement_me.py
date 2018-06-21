from dateutil import parser as date_parser
from elasticsearch.helpers import bulk
from elastic_handler import get_elastic_client

INDEX_NAME = 'entry-index'
ENTRY_TYPE = 'ip_entry'
MAX_DOCUMENTS = 100000
BULK_SIZE = 1000

es = get_elastic_client()


def clear_index():
    if es.indices.exists(INDEX_NAME):
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
    es.indices.create(INDEX_NAME, index_mapping)


def index(data):
    """
    Index the given entries.

    :note: May be called multiple times.

    :param data: A list of 'Entry' instances to index.
    """
    documents = []
    for entry in data:
        doc = dict(entry._asdict())
        doc['_type'] = ENTRY_TYPE
        doc['_index'] = INDEX_NAME
        documents.append(doc)
        # Index in bulks.
        if len(documents) == BULK_SIZE:
            bulk(es, documents)
            documents.clear()

    bulk(es, documents)
    es.indices.flush()
    es.indices.refresh(index=INDEX_NAME)


def get_device_histogram(ip, n):
    """
    Return the latest 'n' entries for the given 'ip'.
    """

    body = {
        'size': n,
        'sort': {
            'timestamp': {
                'order': 'desc'
            }
        },
        'query': {
            'match': {'ip': ip}
        }

    }

    res = es.search(INDEX_NAME, ENTRY_TYPE, body)
    hits = res['hits']['hits']
    return [{'timestamp': date_parser.parse(ip['_source']['timestamp']), 'protocol': ip['_source']['protocol']}
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

    res = es.search(INDEX_NAME, ENTRY_TYPE, get_ips_latest_timestamp)
    buckets = res['aggregations'][ip_grouping_key]['buckets']

    return [(ip['key'], date_parser.parse(ip[latest_timestamp_key]['value_as_string'], ignoretz=True)) for ip in buckets]