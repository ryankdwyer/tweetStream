import redis

class Redis:
    def __init__(self, host='127.0.0.1', port='6379'):
        self.host = host
        self.port = port

    def build_redis(self):
        return redis.Redis(host=self.host, port=self.port)

