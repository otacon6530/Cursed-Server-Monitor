from functions.getDBConnection import getDBConnection
from flask import jsonify, request

def get_metrics():
    server = request.args.get('server')

    conn = getDBConnection()
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
            'status': "pending",
        }
        # No rows returned
        return jsonify(data)

    data = {
        'uptime': rows[0]['Uptime'],
        'cpu_percent': rows[0]['CPUUsage'],
        'memory_percent': rows[0]['RAMUsage'],
        'disk_percent': rows[0]['DiskUsage'],
        'status': rows[0]['Status'],
    }
    return jsonify(data)
