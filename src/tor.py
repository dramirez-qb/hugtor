import os

import hug
from stem import Signal
from stem.control import Controller


class TorController(object):
    def __init__(self,
                 api,
                 app_port,
                 hidden_service_port=80,
                 app_hidden_service_key_path='my_service_key'):
        self.app_port = app_port
        self.hidden_service_port = hidden_service_port
        self.key_path = os.path.expanduser(app_hidden_service_key_path)
        self.controller = Controller.from_port()
        self.service = None

        @hug.get("/healthz")
        def healthz():
            """Adds Health check to the api"""
            return {"alive": True}

        @hug.startup()
        def init_data(api):
            """Adds initial data to the api on startup"""
            self.start()

        self.app = hug.API(__name__)
        self.app.extend(api)
        self.__hug_wsgi__ = self.app.http.server()

    def start(self) -> None:
        """ Function doc https://stem.torproject.org/tutorials/over_the_river.html#ephemeral-hidden-services"""
        self.controller.authenticate()
        self.controller.signal(Signal.NEWNYM)

        if not os.path.exists(self.key_path):
            self.service = self.controller.create_ephemeral_hidden_service(
                {self.hidden_service_port: self.app_port},
                await_publication=True)
            print("Started a new hidden service with the address of %s.onion" %
                  self.service.service_id)

            with open(self.key_path, 'w') as key_file:
                key_file.write(
                    '%s:%s' %
                    (self.service.private_key_type, self.service.private_key))
        else:
            with open(self.key_path) as key_file:
                key_type, key_content = key_file.read().split(':', 1)

            self.service = self.controller.create_ephemeral_hidden_service(
                {self.hidden_service_port: self.app_port},
                key_type=key_type,
                key_content=key_content,
                await_publication=True)
            print("Resumed tor hidden service %s.onion" %
                  self.service.service_id)

    def stop(self) -> None:
        """ Function doc https://stem.torproject.org/tutorials/over_the_river.html#ephemeral-hidden-services"""
        self.controller.authenticate()
        self.controller.remove_ephemeral_hidden_service(
            self.service.service_id)
        print('Shutting down: the hidden service...')

    def __repr__(self):
        return self.controller.list_ephemeral_hidden_services(
            self.service.service_id)
