import redis

from settings import REDIS


def get_redis_client(conf=REDIS):
    print('redis: %s' % conf['host'])
    return redis.StrictRedis(host=conf['host'], port=conf['port'], db=conf['db'], password=conf['password'])


rs = get_redis_client()
