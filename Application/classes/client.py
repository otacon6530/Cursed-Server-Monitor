
from .abstract.application import Application

class Client(Application):
    def __init__(self, args):
        super().__init__(args)  # Call Application's constructor if needed
        try:
            self.connect_to_server(self.host, self.port)
        except ConnectionError as e:
            self.logger.error(f"[Client] {e}")