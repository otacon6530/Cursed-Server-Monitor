from functions.module1 import get_db_connection
from flask import Flask, jsonify, render_template, request
import platform
import pyodbc
from metric_modules import get_cpu_usage, get_rsnapshots, get_uptime, get_all_services_status, get_service_status

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
