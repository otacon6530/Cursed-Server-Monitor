import threading
from datetime import datetime

clients = []
clients_lock = threading.Lock()

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        with clients_lock:
            clients.append(conn)
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp}]{addr}>{data.decode()}")
                # Echo back to sender
                conn.sendall(data)
        finally:
            with clients_lock:
                clients.remove(conn)