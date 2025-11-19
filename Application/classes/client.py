import socket
import threading
from functions.receive_messages import receive_messages

class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.receive_messages = receive_messages
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_thread = threading.Thread(target=self.receive_messages, args=(self.socket,), daemon=True)

    def start(self):
        self.socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
        self.recv_thread.start()
        try:
            while True:
                msg = input(">>")
                if msg.lower() == 'exit':
                    break
                self.socket.sendall(msg.encode())
        finally:
            self.socket.close()

def start_client(host='127.0.0.1', port=65432):
    client = Client(host, port)
    client.start()