from functions.getCPUUsage import getCPUUsage
from functions.getDiskUsage import getDiskUsage
from functions.getRAMUsage import getRAMUsage
from functions.getUpTime import getUpTime
import platform
import requests
from datetime import datetime
import time

metrics_buffer = []

API_URL = "http://localhost:5000/api/metrics"  # Adjust if your API runs elsewhere

def pushMetricsForLocal():
    server = platform.node()
    ram = getRAMUsage()
    cpu = getCPUUsage()
    disk = getDiskUsage()
    uptime = getUpTime()
    datetime_utc = datetime.utcnow().isoformat()  # ISO 8601 format, UTC

    metrics_buffer.append({
        "server": server,
        "RAMUsage": ram,
        "CPUUsage": cpu,
        "DiskUsage": disk,
        "Uptime": uptime,
        "DateTime": datetime_utc
    })

    if len(metrics_buffer) >= 2:
        try:
            response = requests.post(API_URL, json=metrics_buffer)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to post metrics: {e}")
        metrics_buffer.clear()