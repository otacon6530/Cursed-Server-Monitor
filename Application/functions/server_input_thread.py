from functions.broadcast_message import broadcast_message

def server_input_thread():
    while True:
        msg = input("Server message (or 'exit' to quit): ")
        if msg.lower() == 'exit':
            print("Shutting down server input thread.")
            break
        broadcast_message(f"SERVER: {msg}")