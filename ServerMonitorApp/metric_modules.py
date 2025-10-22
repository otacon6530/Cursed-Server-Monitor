# metric_modules.py
import psutil
import subprocess
import platform
import re
import datetime
import sys
import requests
import pyodbc

SYSTEMCTL = "/usr/bin/systemctl"  # full path to systemctl

def get_services():
    try:
        result = subprocess.run(
            [SYSTEMCTL, 'list-units', '--type=service', '--all', '--no-pager', '--no-legend'],
            capture_output=True,
            text=True
        )
        return result
    except Exception as e:
        return {"[EXCEPTION]": str(e)}


def get_all_services_status():
    try:
        result = get_services()
        service_status = {}
        for line in result.stdout.strip().split('\n'):
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 4:
                name = parts[0]
                status = parts[3]
                service_status[name] = status
        return service_status
    except Exception as e:
        return {"[EXCEPTION]": str(e)}


def get_service_status(service):
    try:
        result = subprocess.run(
            [SYSTEMCTL, 'is-active', service],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[EXCEPTION] {e}"

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('/').percent

def get_cpu_usage():
    cpu_usages = psutil.cpu_percent(interval=1, percpu=True)
    average_usage = sum(cpu_usages) / len(cpu_usages)
    return round(average_usage, 1)

def get_uptime():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    return str(uptime).split('.')[0]

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

#TrueNas API
def get_truenas_ram():
    API_KEY = "1-jWlpV3BLbDgiqKnABYYEBS5ZVAMoKRHNbYsEHuInC2zGwISbO5L7ZoBG7MZ61uOv"
    url = "http://10.10.10.110/api/v2.0/system/info"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    total_ram_gb = data['physmem'] / 1024**3
    return total_ram_gb

# Need to move database configuration to a separate config file
DB_CONFIG = {
    'server': 'home.stephensdev.com',
    'database': 'ServerMonitor',
    'username': 'ServerMonitor',
    'password': '*Server*Star*',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'port': 1433
}

sql_server_drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
if not sql_server_drivers:
    raise RuntimeError("No SQL Server ODBC driver found. Please install one.")
DB_CONFIG['driver'] = f'{{{sql_server_drivers[0]}}}'

def execute_sql_query(query, params=None):
    """
    Execute a SQL query string with optional parameters.
    Returns fetched results if available, otherwise None.
    """
    try:
        conn = pyodbc.connect(
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']},{DB_CONFIG['port']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['username']};"
            f"PWD={DB_CONFIG['password']};"
            "Encrypt=no;"
        )
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        # Try to fetch results if any
        try:
            results = cursor.fetchall()
        except pyodbc.ProgrammingError:
            results = None
        conn.commit()
        conn.close()
        return results
    except pyodbc.Error as e:
        print("Database error:", e)
    except Exception as ex:
        print("General error:", ex)
    return None

def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode == 0  # True if ping succeeded