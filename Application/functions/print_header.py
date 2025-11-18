import curses

def print_header(stdscr, host="host", port="port"):
    max_y, max_x = stdscr.getmaxyx()
    curses.resize_term(max_y, max_x)
    stdscr.move(0, 0)
    stdscr.clrtoeol()
    menu = " File  Edit "
    host_port = f"Host: {host} | Port: {port} | Max: {max_x}"
    host_port_x = max_x - len(host_port) - 1
    if host_port_x > len(menu):
        middle = " " * (host_port_x - len(menu))
        header = f"{menu}{middle}{host_port}"
    else:
        header = f"{menu}{host_port}"
    header = header.ljust(max_x - 1)
    stdscr.addstr(0, 0, header, curses.A_REVERSE)
    stdscr.refresh()