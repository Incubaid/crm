from rq import Queue, Connection, Worker
from crm import app
from crm.rq import conn, redis_url


@app.cli.command()
def rq_worker():
    listen = ['default']

    print('Connecting to redis on %s' % redis_url)
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()