from functions.module1 import get_db_connection
from flask import Flask, jsonify, render_template, request
import platform
import pyodbc
from metric_modules import get_cpu_usage, get_rsnapshots, get_uptime, get_all_services_status, get_service_status

def set_metrics():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({'status': 'error', 'message': 'Payload must be a list of metric objects'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 1: Ensure all servers exist
    servers = set(record.get('server') for record in data if record.get('server'))
    if not servers:
        conn.close()
        return jsonify({'status': 'error', 'message': 'No valid server names provided'}), 400

    # Find existing servers
    cursor.execute(
        f"SELECT [Server] FROM [dbo].[Server] WHERE [Server] IN ({','.join(['?']*len(servers))})",
        tuple(servers)
    )
    existing_servers = set(row[0] for row in cursor.fetchall())
    missing_servers = servers - existing_servers

    # Insert missing servers
    if missing_servers:
        cursor.executemany(
            "INSERT INTO [dbo].[Server] ([Server]) VALUES (?)",
            [(s,) for s in missing_servers]
        )
        conn.commit()

    # Step 2: Fetch ServerIds for all servers
    cursor.execute(
        f"SELECT [Server], [ServerId] FROM [dbo].[Server] WHERE [Server] IN ({','.join(['?']*len(servers))})",
        tuple(servers)
    )
    server_id_map = {row[0]: row[1] for row in cursor.fetchall()}

    # Step 3: Prepare bulk insert data for [log].[Server]
    bulk_metrics = []
    for record in data:
        server = record.get('server')
        ram_usage = record.get('RAMUsage', -1)
        cpu_usage = record.get('CPUUsage', -1)
        disk_usage = record.get('DiskUsage', -1)
        uptime = record.get('Uptime', '')
        DateTime = record.get('DateTime', '')
        server_id = server_id_map.get(server)
        if server_id:
            bulk_metrics.append((server_id, ram_usage, cpu_usage, disk_usage, DateTime))
            # Update uptime for each server
            cursor.execute(
                "UPDATE [dbo].[Server] SET [Uptime] = ? WHERE [Server] = ?",
                (uptime, server)
            )

    # Step 4: Bulk insert metrics
    if bulk_metrics:
        cursor.executemany(
            "INSERT INTO [log].[Server] ([ServerId], [RAMUsage], [CPUUsage], [DiskUsage], [InsertDate]) VALUES (?, ?, ?, ?, ?)",
            bulk_metrics
        )

    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})