import pyodbc

class Database:
    def __init__(self, server, database, username=None, password=None):
        sql_server_drivers = [d for d in pyodbc.drivers() if "SQL Server" in d]
        if not sql_server_drivers:
            raise RuntimeError("No SQL Server ODBC driver found. Please install one.")
        self.driver = f'{{{sql_server_drivers[0]}}}'
        self.driver = '{ODBC Driver 17 for SQL Server}' #This work for localdb connections
        if username and password:
            self.conn_str = (
                f"DRIVER={self.driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
            )
        else:
            self.conn_str = (
                f"DRIVER={self.driver};SERVER={server};DATABASE={database};Trusted_Connection=yes"
            )
        self.connection = pyodbc.connect(self.conn_str)
        self.cursor = self.connection.cursor()

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
        self.cursor.execute(
            "SELECT COUNT(*) FROM dbo.server WHERE server = ?", (server_name,)
        )
        exists = self.cursor.fetchone()[0]
        if not exists:
            self.insert("dbo.server", {"server": server_name})
