import socket
import threading
from classes.event_bus import EventBus
from functions.server_input_thread import server_input_thread
from functions.handle_client import handle_client
from classes.header import Header

class Window:
    def __init__(self, host='0.0.0.0', port=65432, stdscr=None):
        self.elements = []
        self.time_events = []
        self.event_bus = EventBus()


        self.shutdown_event = threading.Event()
        self.server_input_thread = server_input_thread
        self.handle_client = handle_client
        self.host = host
        self.port = port
        self.stdscr = stdscr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.input_thread = threading.Thread(target=self.server_input_thread, args=(self,), daemon=True)
        self.header = Header(host, port)
        self.header.draw(self.stdscr)
    def start(self):
        self.input_thread.start()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while not self.shutdown_event.is_set():
                self.socket.settimeout(1.0)  # So accept() doesn't block forever
                try:
                    conn, addr = self.socket.accept()
                    print(f"Connected by {addr}")
                    client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                    client_thread.start()
                    # Example: publish an event when a client connects
                    self.event_bus.publish("client_connected", addr)
                except socket.timeout:
                    continue
        finally:
            self.socket.close()

def start_server(host='0.0.0.0', port=65432):
    server = Window(host, port)
    server.start()