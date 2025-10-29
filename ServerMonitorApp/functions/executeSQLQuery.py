import pyodbc

# Need to move database configuration to a separate config file
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

def executeSQLQuery(query, params=None):
    """
    Execute a SQL query string with optional parameters.
    Returns fetched results if available, otherwise None.
    """
    try:
        conn = pyodbc.connect(
            f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']},{DB_CONFIG['port']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['username']};"
            f"PWD={DB_CONFIG['password']};"
            "Encrypt=no;"
        )
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        # Try to fetch results if any
        try:
            results = cursor.fetchall()
        except pyodbc.ProgrammingError:
            results = None
        conn.commit()
        conn.close()
        return results
    except pyodbc.Error as e:
        print("Database error:", e)
    except Exception as ex:
        print("General error:", ex)
    return None
