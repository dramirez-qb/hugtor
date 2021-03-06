# -*- coding: utf-8 -*-
import atexit
import os

from .app import api
from .tor import TorController

__version__ = '0.0.1'

APP_PORT = os.environ.get('APP_PORT', 5055)
APP_HIDDEN_SERVICE_PORT = os.environ.get('APP_HIDDEN_SERVICE_PORT', 80)
APP_HIDDEN_SERVICE_KEY_PATH = os.environ.get('APP_HIDDEN_SERVICE_KEY_PATH',
                                             'my_service_key')

controler = TorController(api, APP_PORT, APP_HIDDEN_SERVICE_PORT,
                          APP_HIDDEN_SERVICE_KEY_PATH)
application = controler.__hug_wsgi__


@atexit.register
def cleanup():
    try:
        controler.stop()
    except Exception:
        pass
