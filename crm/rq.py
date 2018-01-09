import os
import redis
from rq import Queue

redis_url  = os.getenv('CACHE_BACKEND_URI')
if redis_url:
    redis_url = redis_url[:-2] + '/1'
else:
    redis_url = 'redis://localhost:6379/1'

conn = redis.from_url(redis_url)

queue = Queue(connection=conn)
