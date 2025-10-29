from functions.getServicesWithStatus import getServicesWithStatus
from functions.executeSQLQuery import executeSQLQuery
import platform

def pushServicesForLocal():
    server = platform.node()
    services = getServicesWithStatus()
    for service in services:
        if service['name'] == '[EXCEPTION]':
            continue
        query = (
            "EXECUTE [dbo].[SetService] "
            "@server = ?, @Service = ?, @Status = ?;"
        )
        params = (server, service['name'], service['status'])
        executeSQLQuery(query, params)