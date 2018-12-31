import redis

rs = redis.StrictRedis(host='localhost')

def clear_keys():
    keys = rs.keys('*')
    for k in keys:
        rs.delete(k.decode())

if __name__ == '__main__':
    clear_keys()
