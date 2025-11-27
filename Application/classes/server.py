from .abstract.application import Application
from functions.handle_client import handle_client
import socket


class Server(Application):
    def __init__(self, args):
        super().__init__(args)
        self.handle_client = handle_client
        self.logger.info(f"Server initialized with args: {args}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)