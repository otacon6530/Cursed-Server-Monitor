import subprocess
import sys
import os

# Terminate any running instance of the executable
subprocess.run(["taskkill", "/IM", "servmon.exe", "/F"])

# Run build script and check for errors
build_result = subprocess.run(["powershell", "./build.ps1"])
if build_result.returncode != 0:
    print("Build failed!")
    sys.exit(1)

exe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "dist", "servmon.exe"))
if not os.path.exists(exe_path):
    print(f"Executable not found: {exe_path}")
    sys.exit(1)

# Run test command
subprocess.run([exe_path, "test"])

# Run start command
subprocess.run([exe_path, "start"])