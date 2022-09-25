import redis

from settings import REDIS


def get_redis_client(conf: str = REDIS):
    print('redis: %s' % conf)
    return redis.Redis.from_url(conf)


rs = get_redis_client()
