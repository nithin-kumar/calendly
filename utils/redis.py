import redis

class RedisClientSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisClientSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
        return cls._instance

    def get_redis_client(self):
        return self.redis_client