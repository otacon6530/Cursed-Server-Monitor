import socket
import threading
import builtins
import curses
from functions.server_input_thread import server_input_thread
from functions.handle_client import handle_client
from functions.print_header import print_header

class Server:
    def __init__(self, host='0.0.0.0', port=65432, stdscr=None):
        self.server_input_thread = server_input_thread
        self.handle_client = handle_client
        self.host = host
        self.port = port
        self.stdscr = stdscr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.input_thread = threading.Thread(target=self.server_input_thread, args=(self.stdscr,), daemon=True)
        print_header(self.stdscr, host, port)


    def start(self):
        self.input_thread.start()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                conn, addr = self.socket.accept()
                print(f"Connected by {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                client_thread.start()
        finally:
            self.socket.close()

def start_server(host='0.0.0.0', port=65432):
    server = Server(host, port)
    server.start()