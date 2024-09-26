import os
from psycogreen.gevent import patch_psycopg

name = 'core_app'
bind = '0.0.0.0:8000'

max_requests = 1000
max_requests_jitter = 50

workers = 4 if os.getenv('ENV', 'PREVIEW') == 'PROD' else 2
worker_class = 'gevent'
worker_tmp_dir = '/dev/shm'
pidfile = '/app/logs/gunicorn.pid'

loglevel = 'info'
errorlog = '/app/logs/gunicorn.log'
accesslog = '/app/logs/access.log'
capture_output = True


def post_fork(server, worker):
    patch_psycopg()
    worker.log.debug("Patched Psycopg2 Greenlet")
