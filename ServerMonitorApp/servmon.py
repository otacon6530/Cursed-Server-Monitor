#!/usr/bin/env python3
import click
import subprocess
import pyodbc
import platform
import importlib

#OS specific code imported decided at run
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
def sql():
    """Query SQL Server"""
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=cloud.stephensdev.com;"
        "DATABASE=ServerMonitor;"
        "UID=ServerMonitor;"
        "PWD={*Server*Star*};"
        "Encrypt=no;"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT GETDATE();")
    print("SQL Server time:", cursor.fetchone()[0])
    conn.close()

if __name__ == "__main__":
    cli()
