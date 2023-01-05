import redis

from django.conf import settings

redis_db = redis.Redis(host=settings.REDIS_HOST,
                       port=settings.REDIS_PORT,
                       password=settings.REDIS_PASSWORD,
                       db=1)
