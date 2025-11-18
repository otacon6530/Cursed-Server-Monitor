import socket
import threading
from functions.server_input_thread import server_input_thread
from functions.handle_client import handle_client

class Server:
    def __init__(self, host='0.0.0.0', port=65432):
        self.server_input_thread = server_input_thread
        self.handle_client = handle_client
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.input_thread = threading.Thread(target=self.server_input_thread, daemon=True)

    def start(self):
        self.input_thread.start()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.host}:{self.port}")
        try:
            while True:
                conn, addr = self.socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                client_thread.start()
        finally:
            self.socket.close()

def start_server(host='0.0.0.0', port=65432):
    server = Server(host, port)
    server.start()