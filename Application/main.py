import argparse
import curses
import sys
import unittest
import logging
from classes.server import Server
from classes.logger import Logger
from classes.logger_test_result import LoggerTestResult

def run_tests(logger):
    logger.info("Running unit tests...")
    loader = unittest.TestLoader()
    tests = loader.discover('functions', pattern='test_*.py')
    suite = unittest.TestSuite(tests)
    result = LoggerTestResult(logger)
    suite.run(result)
    if result.wasSuccessful():
        logger.info("All unit tests passed.")
    else:
        logger.error("Some unit tests failed.")
    return result.wasSuccessful()

def main(stdscr):
    parser = argparse.ArgumentParser(description="Start server or client.")
    parser.add_argument("--type", choices=["server", "client"], default="server", help="Mode: server or client (default: server)")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=4536, help="Port (default: 4536)")
    parser.add_argument("--test", action="store_true", help="Run unit tests before starting the program")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase output verbosity (use -v, -vv, or -vvv)")

    args = parser.parse_args()

    # Set error_level based on verbosity
    if args.verbose >= 3:
        error_level = logging.DEBUG
    elif args.verbose == 2:
        error_level = logging.INFO
    elif args.verbose == 1:
        error_level = logging.WARNING
    else:
        error_level = logging.ERROR

    args.logger = Logger("Cursed Monitor", level=error_level)
    args.logger.debug("Logger initialized with level: %s", logging.getLevelName(error_level))
    args.logger.info("Starting application with arguments: %s", args)

    if args.test:
        args.logger.info("Test mode enabled. Running tests before starting application.")
        success = run_tests(args.logger)
        if not success:
            args.logger.error("Exiting due to failed unit tests.")
            sys.exit("Unit tests failed. Exiting.")

    args.stdscr = stdscr
    try:
        if args.type == "server":
            args.logger.info("Starting server on %s:%d", args.host, args.port)
            server = Server(args)
            server.start()
        elif args.type == "client":
            args.logger.info("Starting client connecting to %s:%d", args.host, args.port)
            server = Server(args)
            server.start()
        else:
            args.logger.error("Unknown type specified: %s", args.type)
            sys.exit(f"Unknown type: {args.type}")
    except Exception as e:
        if hasattr(args, 'logger') and args.logger:
            args.logger.exception("Fatal error occurred: %s", e)
        else:
            print(f"Fatal error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        # Fallback logging if logger is not available
        print(f"Unhandled exception: {e}")