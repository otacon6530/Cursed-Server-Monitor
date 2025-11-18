import argparse
import curses
from functions.print_header import print_header
from classes.start_server import Server
from classes.start_client import Client

def main(stdscr):
    parser = argparse.ArgumentParser(description="Start server or client.")
    parser.add_argument("--type", choices=["server", "client"], default="server", help="Mode: server or client (default: server)")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=4536, help="Port (default: 4536)")
    args = parser.parse_args()
    if args.type == "server":
        server = Server(args.host, args.port, stdscr)
        server.start()
    else:
        client = Client(args.host, args.port)
        client.start()

if __name__ == "__main__":
    curses.wrapper(main)