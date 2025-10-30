from functions.getDBConnection import getDBConnection
from flask import jsonify

def get_cpu_usage_history(limit=10):
    conn = getDBConnection()
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
