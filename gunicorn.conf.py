"""
Common gunicorn configuration
"""
import os

bind = "0.0.0.0:" + str(os.environ.get('APP_PORT', 5055))
workers = 1
threads = os.environ.get('APP_THREADS', 1)
timeout = 120
preload_app = True
loglevel = os.environ.get('LOGLEVEL', 'info')
reload = False if os.environ.get('APP_ENV', 'prod') else True
accesslog = '-'
errorlog = '-'
