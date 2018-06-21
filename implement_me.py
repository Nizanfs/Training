import pymongo
from pymongo import MongoClient

MONGO_PORT = 27017
DB_NAME = 'test'
COLLECTION_NAME = 'ips'
BULK_SIZE = 1000


mongo_client = MongoClient('localhost', MONGO_PORT)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]


def clear_collection():
    collection.remove()


def index(data):
    """
    Index the given entries.

    :note: May be called multiple times.

    :param data: A list of 'Entry' instances to index.
    """
    documents = []
    for entry in data:
        doc = dict(entry._asdict())
        documents.append(doc)
        # Insert in bulks.
        if len(documents) == BULK_SIZE:
            collection.insert_many(documents)
            documents.clear()

    collection.insert_many(documents)


def get_device_histogram(ip, n):
    """
    Return the latest 'n' entries for the given 'ip'.
    """
    results = collection.find({'ip': ip}).sort('timestamp', pymongo.DESCENDING).limit(n)
    return [{'timestamp': ip['timestamp'], 'protocol': ip['protocol']} for ip in results]


def get_devices_status():
    """
    Return a list of every ip and the latest time it was seen it.
    """
    pipeline = [
        {
            '$group': {
                '_id' : '$ip',
                'latest_timestamp': {
                    '$max': '$timestamp'
                }
            }
        }
    ]

    results = collection.aggregate(pipeline)

    return [(entry['_id'], entry['latest_timestamp']) for entry in results]