import platform
import subprocess
from functions.ping import ping
from functions.executeSQLQuery import executeSQLQuery

def pushMetricsForURL(server_url):
    if ping(server_url):
        query = (
            "EXECUTE [dbo].[SetServerMetrics] "
            "@Server = ?;"
        )
        params = (server_url,)
        executeSQLQuery(query, params)
