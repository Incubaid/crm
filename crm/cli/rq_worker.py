import os
import redis
from rq import Queue, Connection, Worker
from crm import app


@app.cli.command()
def rq_worker():
    listen = ['default']
    redis_url  = os.getenv('CACHE_BACKEND_URI')
    if redis_url:
        redis_url = redis_url[:-2] + '/1'
    else:
        redis_url = 'redis://localhost:6379/1'

    conn = redis.from_url(redis_url)
    print('Connecting to redis on %s' % redis_url)
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()