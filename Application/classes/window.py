import socket
import threading
from classes.time_event_manager import TimeEventManager
from functions.server_input_thread import server_input_thread
from functions.handle_client import handle_client
from classes.header import Header
from classes.database import Database
from functions.get_server_name import get_computer_name
from functions.getCPUUsage import getCPUUsage
from functions.getDiskUsage import getDiskUsage
from functions.getRAMUsage import getRAMUsage
import os
import time

DB_CONFIG = {
    'server': '(localdb)\\ProjectModels',
    'database': 'ServerMonitor'
}

class Window:
    def __init__(self, args):
        self.host = getattr(args, 'host', '0.0.0.0')
        self.port = getattr(args, 'port', 65432)
        self.name = get_computer_name()
        self.stdscr = getattr(args, 'stdscr', None)
        self.time_event_manager = TimeEventManager()
        self.shutdown_event = threading.Event()
        self.server_input_thread = server_input_thread
        self.handle_client = handle_client
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.input_thread = threading.Thread(target=self.server_input_thread, args=(self,), daemon=True)
        self.header = Header(self)  
        self.run_database_function(lambda db: db.insert_server_if_not_exists(self.name))
        self.metrics_thread = threading.Thread(target=self.metrics_worker, daemon=True)
        self.CPUUsage = 0
        self.RAMUsage = 0
        self.DiskUsage = 0  
    
    def start(self):
        self.input_thread.start()
        self.metrics_thread.start()
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while not self.shutdown_event.is_set():
                self.header.draw(self.stdscr, self)
                self.socket.settimeout(1.0)  # So accept() doesn't block forever
                self.time_event_manager.tick()
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
            self.shutdown_event.set()
            self.socket.close()

    def metrics_worker(self):
        while not self.shutdown_event.is_set():
            self.save_metrics()
            time.sleep(5)

    def save_metrics(self):
        """
        Retrieves metrics from the database for this server.
        Returns:
            A list of metrics.
        """
        self.CPUUsage = getCPUUsage()
        self.RAMUsage = getRAMUsage()
        self.DiskUsage = getDiskUsage()
        row = {
            "CPUUsage": self.CPUUsage
          , "RAMUsage": self.RAMUsage
          , "DiskUsage": self.DiskUsage
        }
        return self.run_database_function(lambda db: db.insert_metrics(self.name, row))

    def run_database_function(self, db_func, *args, **kwargs):
        """
        Creates a Database object, runs the provided database function, and closes the connection.

        Args:
            db_func: A callable that accepts a Database instance as its first argument.
            *args, **kwargs: Additional arguments to pass to db_func.
        Returns:
            The result of db_func.
        """
        db = Database(server=DB_CONFIG['server'], database=DB_CONFIG['database'])
        try:
            result = db_func(db, *args, **kwargs)
        finally:
            db.close()
        return result

if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 3)  # 3 = SW_MAXIMIZE

