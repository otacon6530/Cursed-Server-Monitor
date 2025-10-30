from functions.getDBConnection import getDBConnection
from flask import jsonify

def get_servers():
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT [server] FROM dbo.server')
    rows = cursor.fetchall()
    conn.close()

    # Convert to a list of server names
    servers = [row[0] for row in rows]
    return jsonify(servers)