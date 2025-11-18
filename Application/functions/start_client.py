import socket
import threading
from functions.receive_messages import receive_messages

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        recv_thread = threading.Thread(target=receive_messages, args=(s,), daemon=True)
        recv_thread.start()
        while True:
            msg = input("Enter message (or 'exit' to quit): ")
            if msg.lower() == 'exit':
                break
            s.sendall(msg.encode())
        s.close()