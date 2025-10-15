from flask import Flask, jsonify, render_template, request
import os
from flask_cors import CORS
import psutil
import platform
import subprocess
import pyodbc
import datetime
from metric_modules import get_cpu_usage, get_rsnapshots, get_uptime, get_all_services_status, get_service_status

app = Flask(__name__)
CORS(app)  # Enable CORS

#Need to move database configuration to a separate config file
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

#Default Web App Page
@app.route("/")
def index():
    return render_template("index.html")

def get_db_connection():
    connection_string = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']},{DB_CONFIG['port']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        "Encrypt=no;"
    )
    return pyodbc.connect(connection_string)

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    server = request.args.get('server')
    service_status = get_all_services_status()

    conn = get_db_connection()
    cursor = conn.cursor()
    print(f'Fetching metrics for server: {server}')
    cursor.execute('EXECUTE [dbo].[GetServerMetrics] @server=?', (server,))
    columns = [column[0] for column in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close();

    if not rows:
        data = {
            'uptime': "",
            'cpu_percent': -1,
            'memory_percent': -1,
            'disk_percent': -1,
            'services': service_status,
        }
        # No rows returned
        return jsonify(data)

    data = {
        'uptime': rows[0]['Uptime'],
        'cpu_percent': rows[0]['CPUUsage'],
        'memory_percent': rows[0]['RAMUsage'],
        'disk_percent': rows[0]['DiskUsage'],
        'services': service_status,
    }
    return jsonify(data)


@app.route('/api/cpu-usage', methods=['GET'])
def get_cpu_usage_history(limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT [InsertDate], UsagePerc
        FROM log.CPU
        ORDER BY [InsertDate] DESC
        OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY
    ''')
    rows = cursor.fetchall()
    conn.close()

    data = [
        {
            'timestamp': "", #row[0].strftime('%Y-%m-%d %H:%M:%S'),
            'cpu_percent': row[1]
        }
        for row in rows
    ]
    return jsonify(data)

@app.route('/api/get-servers', methods=['GET'])
def get_servers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT [server] FROM dbo.server')
    rows = cursor.fetchall()
    conn.close()

    # Convert to a list of server names
    servers = [row[0] for row in rows]
    return jsonify(servers)


@app.route('/api/hostname', methods=['GET'])
def get_hostname():
    data = {
        'hostname': platform.node(),
    }
    return jsonify(data)


@app.route('/api/rsnap', methods=['GET'])
def get_rsnap():
    data = get_rsnapshots()
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)