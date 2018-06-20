from elasticsearch import Elasticsearch
import docker
import time

ELASTIC_PORT = f'9200'


def start_elastic():
    client = docker.from_env()
    container = client.containers.run('elasticsearch', ports={ELASTIC_PORT: ELASTIC_PORT}, detach=True, remove=True)
    # Stop the code execution until the elastic-docker is up.
    logs = container.logs(stream=True, tail=2)
    while not (next(logs).endswith(b'started\n')):
        time.sleep(1)
        logs = container.logs(stream=True, tail=2)

    return container


def close_elastic(elastic):
    elastic.stop()


def get_elastic_client():
    return Elasticsearch(f'http://localhost:%s' % ELASTIC_PORT)
