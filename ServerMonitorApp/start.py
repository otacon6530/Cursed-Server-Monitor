import subprocess
import sys
import os

exe_path = os.path.join(os.path.dirname(__file__), "dist", "servmon.exe")
args = ["sql"]

subprocess.run([exe_path] + args)