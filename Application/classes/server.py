from .abstract.application import Application

class Server(Application):
    def __init__(self, args):
        super().__init__(args)  # Call Application's constructor if needed
        print("Server initialized with args:", args)