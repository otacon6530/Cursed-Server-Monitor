#!/usr/bin/env python3
import click
import subprocess
import pyodbc
import platform
import importlib
import psutil
import time
from metric_modules import get_cpu_usage

# OS specific code imported decided at run
if platform.system() == "Windows":
    module_name = "windows"
else:
    module_name = "linux"

os = importlib.import_module(module_name)

@click.group()
def cli():
    pass

@cli.command()
@click.argument("cmd", nargs=-1)
def run(cmd):
    """Run a system command"""
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    print(result.stdout)

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

@cli.command()
def sql():
    """Query SQL Server in an infinite loop every 5 seconds"""
    while True:
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
            Server = platform.node()
            RAMUsage = psutil.virtual_memory().percent
            CPUusage = get_cpu_usage()
            DiskUsage = psutil.disk_usage('/').percent

            query = (
                "EXECUTE [dbo].[SetServerMetrics] "
                "@Server = ?, @RAMUsage = ?, @CPUusage = ?, @DiskUsage = ?;"
            )
            params = (Server, RAMUsage, CPUusage, DiskUsage)

            cursor.execute(query, params)
            conn.commit()
            conn.close()
        except pyodbc.Error as e:
            print("Database error:", e)
        except Exception as ex:
            print("General error:", ex)
        time.sleep(5)

if __name__ == "__main__":
    cli()
