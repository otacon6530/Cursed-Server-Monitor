import socket

def get_computer_name() -> str:
    """
    Returns the current computer's network name.
    """
    return socket.gethostname()