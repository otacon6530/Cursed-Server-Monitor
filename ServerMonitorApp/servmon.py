#!/usr/bin/env python3
import click
import subprocess
import pyodbc
import platform
import importlib
import psutil
import time
from metric_modules import get_cpu_usage, execute_sql_query, get_uptime, get_ram_usage, get_disk_usage

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

@cli.command()
def test():
    """Testing functions"""
    print(f"Uptime: {get_uptime()}")
    print(f"CPU Usage: {get_cpu_usage()}")
    print(f"RAM Usage: {get_ram_usage()}")
    print(f"Disk Usage: {get_disk_usage()}")

@cli.command()
def sql():
    """Query SQL Server in an infinite loop every 5 seconds"""
    while True:
        Server = platform.node()
        RAMUsage = get_ram_usage()
        CPUusage = get_cpu_usage()
        DiskUsage = get_disk_usage()
        Uptime = get_uptime()

        query = (
            "EXECUTE [dbo].[SetServerMetrics] "
            "@Server = ?, @RAMUsage = ?, @CPUusage = ?, @DiskUsage = ?, @Uptime = ?;"
        )
        params = (Server, RAMUsage, CPUusage, DiskUsage, Uptime)
        execute_sql_query(query,params)
        time.sleep(5)

if __name__ == "__main__":
    cli()
