import argparse
import curses
from classes.window import Window

def main(stdscr):
    parser = argparse.ArgumentParser(description="Start server or client.")
    parser.add_argument("--type", choices=["server", "client"], default="server", help="Mode: server or client (default: server)")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=4536, help="Port (default: 4536)")
    args = parser.parse_args()
    args.stdscr = stdscr
    if args.type == "server":
        server = Window(args)
        server.start()

if __name__ == "__main__":
    curses.wrapper(main)