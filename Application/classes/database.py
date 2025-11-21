import pyodbc
import sqlite3
from classes.event_bus import event_bus

class Database:
    def __init__(self, server, database, username=None, password=None, sqlite_path="local.db"):
        self.use_sqlite = False
        try:
            sql_server_drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
            if not sql_server_drivers:
                raise RuntimeError("No SQL Server ODBC driver found. Please install one.")
            self.driver = '{ODBC Driver 17 for SQL Server}'
            if username and password:
                self.conn_str = (
                    f"DRIVER={self.driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
                )
            else:
                self.conn_str = (
                    f"DRIVER={self.driver};SERVER={server};DATABASE={database};Trusted_Connection=yes"
                )
            self.connection = pyodbc.connect(self.conn_str, timeout=3)
            self.cursor = self.connection.cursor()
            event_bus.publish("update_database_status", True)
        except Exception as ex:
            print("SQL Server unavailable, switching to SQLite:", ex)
            self.use_sqlite = True
            self.connection = sqlite3.connect(sqlite_path)
            self.cursor = self.connection.cursor()
            self._ensure_sqlite_schema()
            event_bus.publish("update_database_status", False)

    def _ensure_sqlite_schema(self):
        # Create tables if they don't exist (example schema, adjust as needed)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS server (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server TEXT UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                server_id INTEGER,
                CPUUsage REAL,
                RAMUsage REAL,
                DiskUsage REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(server_id) REFERENCES server(id)
            )
        """)
        self.connection.commit()

    def insert(self, table, data):
        """
        Insert data into table.
        data: dict for single row, or list of dicts for multiple rows.
        Example: insert("Users", {"Name": "John", "Age": 30})
                 insert("Users", [{"Name": "John", "Age": 30}, {"Name": "Jane", "Age": 25}])
        """
        if isinstance(data, dict):
            data = [data]
        if not data:
            return

        columns = ', '.join(data[0].keys())
        placeholders = ', '.join(['?' for _ in data[0]])
        values_list = [list(row.values()) for row in data]
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.executemany(sql, values_list)
        self.connection.commit()

    def read(self, table, columns="*", where=None):
        """
        Read data from table.
        columns: list or string of columns to select.
        where: optional SQL WHERE clause (string).
        Example: read("Users", ["Name", "Age"], "Age > 20")
        """
        if isinstance(columns, list):
            columns = ', '.join(columns)
        sql = f"SELECT {columns} FROM {table}"
        if where:
            sql += f" WHERE {where}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def executeSQLQuery(self, query, params=None):
        """
        Execute a SQL query string with optional parameters.
        Returns fetched results if available, otherwise None.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            # Try to fetch results if any
            try:
                results = self.cursor.fetchall()
            except pyodbc.ProgrammingError:
                results = None
            return results
        except pyodbc.Error as e:
            print("Database error:", e)
        except Exception as ex:
            print("General error:", ex)
        return None

    def close(self):
        self.cursor.close()
        self.connection.close()

    def insert_server_if_not_exists(self, server_name):
        """
        Inserts the server_name into dbo.server if it does not already exist.
        """
        if self.use_sqlite:
            self.cursor.execute("SELECT COUNT(*) FROM server WHERE server = ?", (server_name,))
            exists = self.cursor.fetchone()[0]
            if not exists:
                self.cursor.execute("INSERT INTO server (server) VALUES (?)", (server_name,))
                self.connection.commit()
        else:
            self.cursor.execute(
                "SELECT COUNT(*) FROM dbo.server WHERE server = ?", (server_name,)
            )
            exists = self.cursor.fetchone()[0]
            if not exists:
                self.insert("dbo.server", {"server": server_name})

    def insert_metrics(self, server_name, values):
        """
        Inserts metrics for a specific server into the database using the server's id.
        """
        # Fetch the server id from dbo.server
        self.cursor.execute(
            "SELECT serverid FROM dbo.server WHERE server = ?", (server_name,)
        )
        row = self.cursor.fetchone()
        if not row:
            raise ValueError(f"Server '{server_name}' not found in dbo.server table.")
        server_id = row[0]

        # Prepare metrics data for insertion
        # Assuming 'values' is an object or dict with metric fields
        # Example: values = {'cpu': 10, 'memory': 20, ...}
        # You may need to adjust this part based on your actual metrics schema
        metrics_data = dict(values) if isinstance(values, dict) else vars(values)
        metrics_data['ServerId'] = server_id

        # Insert metrics into dbo.metrics (adjust table/columns as needed)
        columns = ', '.join(metrics_data.keys())
        placeholders = ', '.join(['?' for _ in metrics_data])
        sql = f"INSERT INTO log.server ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, list(metrics_data.values()))
        self.connection.commit()