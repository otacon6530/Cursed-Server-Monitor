from functions.handle_client import clients, clients_lock

def broadcast_message(message):
    with clients_lock:
        for client in clients:
            try:
                client.sendall(message.encode())
            except Exception:
                pass  # Ignore errors for disconnected clients