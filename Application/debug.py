import subprocess
import sys
import time
import os

main_py = "main.py"
def run_in_new_terminal(args, title=""):
    # Always quote the title argument
    if not title:
        title = ""
    cmd = ["start", title, sys.executable] + args
    print("Running command:", cmd)  # Print the command for debugging
    return subprocess.Popen(cmd, shell=True)

# Start the server in a new terminal
server_args = [main_py, "--type", "server"]
server_proc = run_in_new_terminal(server_args, "Server")
print("Server started in new terminal.")

time.sleep(2)

server_args2 = [main_py, "--type", "client"]
server_proc2 = run_in_new_terminal(server_args, "Client")
print("Server started in new terminal.")