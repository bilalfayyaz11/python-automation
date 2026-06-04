import os

class Config:
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    API_PORT = int(os.getenv('API_PORT', 5000))

    @staticmethod
    def get_redis_url():
        return f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}"
