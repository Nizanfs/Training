import docker
import redis

REDIS_PORT = 6379


def start_redis():
    client = docker.from_env()
    container = client.containers.run('redis', ports={REDIS_PORT: REDIS_PORT}, detach=True, remove=True)
    return container


def close_redis(redis_container):
    redis_container.stop()


def get_redis_client():
    return redis.StrictRedis(host='localhost', port=REDIS_PORT)
