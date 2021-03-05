import os
from stem.control import Controller

class TorController(object):

    def __init__ (self, app_port, hidden_service_port = 80, app_hidden_service_key_path = 'my_service_key'):
        self.app_port = app_port
        self.hidden_service_port = hidden_service_port
        self.key_path = os.path.expanduser(app_hidden_service_key_path)
        self.controller = Controller.from_port()
        self.service = None

    def start(self)-> None:
      """ Function doc https://stem.torproject.org/tutorials/over_the_river.html#ephemeral-hidden-services"""
      self.controller.authenticate()

      if not os.path.exists(self.key_path):
        self.service = self.controller.create_ephemeral_hidden_service({self.hidden_service_port: self.app_port}, await_publication = True)
        print("Started a new hidden service with the address of %s.onion" % self.service.service_id)

        with open(self.key_path, 'w') as key_file:
          key_file.write('%s:%s' % (self.service.private_key_type, self.service.private_key))
      else:
        with open(self.key_path) as key_file:
          key_type, key_content = key_file.read().split(':', 1)

        self.service = self.controller.create_ephemeral_hidden_service({self.hidden_service_port: self.app_port}, key_type = key_type, key_content = key_content, await_publication = True)
        print("Resumed %s.onion" % self.service.service_id)

    def stop(self)-> None:
      """ Function doc https://stem.torproject.org/tutorials/over_the_river.html#ephemeral-hidden-services"""
      self.controller.authenticate()
      self.controller.remove_ephemeral_hidden_service(self.service.service_id)
      print('shut the service down...')

    def __repr__(self):
        pass

