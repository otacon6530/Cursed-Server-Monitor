import argparse
from classes.start_server import Server
from functions.start_client import start_client

def main():
    parser = argparse.ArgumentParser(description="Start server or client.")
    parser.add_argument("--type", choices=["server", "client"], default="server", help="Mode: server or client (default: server)")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=4536, help="Port (default: 4536)")
    args = parser.parse_args()
    if args.type == "server":
        server = Server(args.host, args.port)
        server.start()
    else:
        start_client(args.host, args.port)

if __name__ == "__main__":
    main()