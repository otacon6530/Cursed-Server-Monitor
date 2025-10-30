import subprocess
import sys
import os

# Start HTTP server in UI folder
ui_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "UI"))
if not os.path.exists(ui_dir):
    print(f"UI directory not found: {ui_dir}")
    sys.exit(1)

print(f"Starting HTTP server in {ui_dir} on port 8000...")
subprocess.Popen([sys.executable, "-m", "http.server", "8000"], cwd=ui_dir)

# Start run.py in API folder
api_dir = os.path.abspath(os.path.dirname(__file__))
runpy_path = os.path.join(api_dir, "run.py")
if not os.path.exists(runpy_path):
    print(f"run.py not found: {runpy_path}")
    sys.exit(1)

print(f"Starting run.py in {api_dir}...")
subprocess.Popen([sys.executable, runpy_path], cwd=api_dir)