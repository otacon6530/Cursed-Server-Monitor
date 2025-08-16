from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import platform
import subprocess
import pyodbc
import datetime
from metric_modules import get_cpu_usage, get_rsnapshots, get_uptime, get_all_services_status, get_service_status

DB_CONFIG = {
    'server': 'localhost',
    'database': 'ServerMonitor',
    'username': 'ServerMonitor',
    'password': '*Server*Star*',
    'driver': '{ODBC Driver 18 for SQL Server}',
    'port': 1433
}

app = Flask(__name__)
CORS(app)  # Enable CORS

SYSTEMCTL = "/usr/bin/systemctl"  # full path to systemctl

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

services = ['apache2', 'mysql', 'docker', 'bedrock-server']

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    uptime = get_uptime()
    #service_status = {svc: get_service_status(svc) for svc in services}
    service_status = get_all_services_status()
    cpu_percent = get_cpu_usage()

    data = {
        'uptime': uptime,
        'cpu_percent': cpu_percent,
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
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
            'timestamp': row[0].strftime('%Y-%m-%d %H:%M:%S'),
            'cpu_percent': row[1]
        }
        for row in rows
    ]
    return jsonify(data)


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