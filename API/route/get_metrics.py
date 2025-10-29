from functions.module1 import get_db_connection
from flask import Flask, jsonify, render_template, request
import platform
import pyodbc
from metric_modules import get_cpu_usage, get_rsnapshots, get_uptime, get_all_services_status, get_service_status

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
            'status': "pending",
        }
        # No rows returned
        return jsonify(data)

    data = {
        'uptime': rows[0]['Uptime'],
        'cpu_percent': rows[0]['CPUUsage'],
        'memory_percent': rows[0]['RAMUsage'],
        'disk_percent': rows[0]['DiskUsage'],
        'services': service_status,
        'status': rows[0]['Status'],
    }
    return jsonify(data)
