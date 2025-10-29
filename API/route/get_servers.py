from functions.module1 import get_db_connection
from flask import Flask, jsonify, render_template, request
import platform
import pyodbc
from metric_modules import get_cpu_usage, get_rsnapshots, get_uptime, get_all_services_status, get_service_status

def get_servers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT [server] FROM dbo.server')
    rows = cursor.fetchall()
    conn.close()

    # Convert to a list of server names
    servers = [row[0] for row in rows]
    return jsonify(servers)