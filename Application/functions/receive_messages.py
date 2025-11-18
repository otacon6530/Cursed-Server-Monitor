def receive_messages(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("Disconnected from server.")
                break
            print(f"\nMessage from server: {data.decode()}\n", end="")
        except Exception:
            break