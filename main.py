# -*- coding: utf-8 -*-

from app import api
from tor import TorController

APP_PORT = 5055
APP_HIDDEN_SERVICE_PORT = 80
APP_HIDDEN_SERVICE_KEY_PATH = 'my_service_key'

if __name__ == "__main__":
    controler = TorController(APP_PORT, APP_HIDDEN_SERVICE_PORT, APP_HIDDEN_SERVICE_KEY_PATH)
    try:
      controler.start()
      api.http.serve(port=APP_PORT)
    except KeyboardInterrupt:
      pass
    finally:
      controler.stop()

