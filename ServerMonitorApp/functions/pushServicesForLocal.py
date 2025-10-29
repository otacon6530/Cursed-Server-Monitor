from functions.getServicesWithStatus import getServicesWithStatus
from functions.executeSQLQuery import executeSQLQuery
import platform
import time
iteration = 0
def pushServicesForLocal():
    global iteration
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
    if iteration >= 1:
        print(f"Pushed services for server: {server}")
        time.sleep(55)
    iteration += 1