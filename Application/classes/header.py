import curses

class Header:
    def __init__(self, window):
        self.host = window.host
        self.port = window.port
        self.name = window.name
        self.it = 0

    def draw(self, stdscr, window):
        self.it += 1
        dbactive = "Disconnected"
        if window.DBActive:
            dbactive = "Connected"
        max_y, max_x = stdscr.getmaxyx()
        curses.resize_term(max_y, max_x)
        menu = f"{self.name}({self.host}:{self.port}) CPU:{window.CPUUsage:05.1f}%  Ram:{window.RAMUsage:05.1f}%  Disk:{window.DiskUsage:05.1f}%  "
        host_port = f"Database:{dbactive} tick:{self.it} "
        host_port_x = max_x - len(host_port) 
        if host_port_x > len(menu):
            middle = " " * (host_port_x - len(menu))
            header = f"{menu}{middle}{host_port}"
        else:
            header = f"{menu}{host_port}"
        header = header.ljust(max_x - 1)
        cur_y, cur_x = stdscr.getyx()
        stdscr.addstr(0, 0, header, curses.A_REVERSE)
        # Restore cursor position
        stdscr.move(cur_y, cur_x)
        stdscr.refresh()