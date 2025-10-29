import pyodbc
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
