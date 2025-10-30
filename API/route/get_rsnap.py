from flask import jsonify
import subprocess
import re

def get_rsnapshots():
    hourly = get_rsnapshot("hourly")
    daily = get_rsnapshot("daily")
    weekly = get_rsnapshot("weekly")
    monthly = get_rsnapshot("monthly")
    data = {
         'hourly': hourly,
         'daily': daily,
         'weekly': weekly,
         'monthly': monthly
    }
    return data

def get_rsnapshot(periodicity):
    cmd = f"/bin/grep '{periodicity}: completed successfully' /var/log/rsnapshot.log | /usr/bin/tail -1"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # Regex to capture the ISO8601-like timestamp inside brackets
    match = re.search(r'\[(.*?)\]', result.stdout.strip())
    if match:
        result = match.group(1)
    else:
        result = ""
    return result

def get_rsnap():
    data = get_rsnapshots()
    return jsonify(data)