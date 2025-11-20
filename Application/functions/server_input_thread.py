import curses

def server_input_thread(server):
    stdscr = server.stdscr
    shutdown_event = server.shutdown_event
    curses.echo()
    messages = []

    def cmd_exit():
        shutdown_event.set()
        return True  # Signal to break loop

    def cmd_help():
        messages.append("Available commands:")
        messages.append("\t[exit/quit]: return to command prompt")
        return False

    commands = {
        "exit": cmd_exit,
        "quit": cmd_exit,
        "help": cmd_help,
    }

    while True:
        max_y, max_x = stdscr.getmaxyx()
        messages = messages[-(max_y - 2):]
        [stdscr.addstr(i + 1, 0, m[:max_x - 1]) or stdscr.clrtoeol() for i, m in enumerate(messages)]
        prompt_row = min(len(messages), max_y - 2) + 1
        stdscr.addstr(prompt_row, 0, ">>")
        stdscr.clrtoeol()
        stdscr.move(prompt_row, 3)  # Ensure cursor is after '>>'
        stdscr.refresh()
        msg = stdscr.getstr(prompt_row, 3).decode().strip()
        cmd = msg.lower()
        messages.append(f">> {msg}")
        if cmd in commands:
            if commands[cmd]():
                break
        else:
            messages.append(f"Unknown command: {cmd}")
            cmd_help()