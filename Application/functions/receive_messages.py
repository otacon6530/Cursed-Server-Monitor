from functions.print_header import print_header
def receive_messages(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("Disconnected from server.")
                break
            print(f"\nMessage from server: {data.decode()}\n", end="")
            print_header("host","port")
        except Exception:
            break