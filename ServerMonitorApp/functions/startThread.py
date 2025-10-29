import threading

def startThread(thread, target, args=None):
    if thread is None or not thread.is_alive():
        if args:
            thread = threading.Thread(target=target, args=args)
        else:
            thread = threading.Thread(target=target)
        thread.start()
    return thread
