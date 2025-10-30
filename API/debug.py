import subprocess
import sys
import os

# Start run.py in API folder
api_dir = os.path.abspath(os.path.dirname(__file__))
runpy_path = os.path.join(api_dir, "run.py")
if not os.path.exists(runpy_path):
    print(f"run.py not found: {runpy_path}")
    sys.exit(1)

print(f"Starting run.py in {api_dir}...")
subprocess.Popen([sys.executable, runpy_path], cwd=api_dir)