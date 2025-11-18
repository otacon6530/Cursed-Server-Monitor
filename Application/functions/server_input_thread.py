import curses
from functions.broadcast_message import broadcast_message
from functions.print_header import print_header

def server_input_thread(stdscr):
    curses.echo()
    while True:
        print_header(stdscr, "test", "test")
        stdscr.addstr(2, 0, "Server message (or 'exit' to quit): ")
        stdscr.clrtoeol()
        stdscr.refresh()
        msg = stdscr.getstr(2, 35).decode()
        if msg.lower() == 'exit':
            stdscr.addstr(3, 0, "Shutting down server input thread.")
            stdscr.refresh()
            break
        broadcast_message(f"SERVER: {msg}")