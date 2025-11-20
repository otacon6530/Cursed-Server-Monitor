import argparse
import curses
import sys
import unittest
from classes.window import Window

def run_tests():
    loader = unittest.TestLoader()
    tests = loader.discover('functions', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    result = runner.run(tests)
    return result.wasSuccessful()

def main(stdscr):
    parser = argparse.ArgumentParser(description="Start server or client.")
    parser.add_argument("--type", choices=["server", "client"], default="server", help="Mode: server or client (default: server)")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=4536, help="Port (default: 4536)")
    parser.add_argument("--test", action="store_true", help="Run unit tests before starting the program")
    args = parser.parse_args()

    if args.test:
        success = run_tests()
        if not success:
            sys.exit("Unit tests failed. Exiting.")

    args.stdscr = stdscr
    if args.type == "server":
        server = Window(args)
        server.start()

if __name__ == "__main__":
    curses.wrapper(main)