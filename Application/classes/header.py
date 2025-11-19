import curses
from datetime import datetime

class Header:
    def __init__(self, stdscr, host="host", port="port"):
        self.host = host
        self.port = port

    def draw(self, stdscr):
        max_y, max_x = stdscr.getmaxyx()
        curses.resize_term(max_y, max_x)
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        menu = " File  Edit - +"
        host_port = f"Host: {self.host} | Port: {self.port} | Max: {max_x}"
        clock = datetime.now().strftime("%H:%M:%S")
        # Position clock at far right
        clock_x = max_x - len(clock) - 1
        host_port_x = clock_x - len(host_port) - 1
        if host_port_x > len(menu):
            middle = " " * (host_port_x - len(menu))
            header = f"{menu}{middle}{host_port}{' ' * (clock_x - len(menu) - len(middle) - len(host_port))}{clock}"
        else:
            header = f"{menu}{host_port}{' ' * (clock_x - len(menu) - len(host_port))}{clock}"
        header = header.ljust(max_x - 1)
        stdscr.addstr(0, 0, header, curses.A_REVERSE)
        stdscr.refresh()