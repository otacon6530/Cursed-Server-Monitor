from functions.getCPUUsage import getCPUUsage
from functions.getDiskUsage import getDiskUsage
from functions.getRAMUsage import getRAMUsage
from functions.getUpTime import getUpTime
from functions.executeSQLQuery import executeSQLQuery
import platform

def pushMetricsForLocal():
    server = platform.node()
    ram = getRAMUsage()
    cpu = getCPUUsage()
    disk = getDiskUsage()
    uptime = getUpTime()
    query = (
        "EXECUTE [dbo].[SetServerMetrics] "
        "@Server = ?, @RAMUsage = ?, @CPUusage = ?, @DiskUsage = ?, @Uptime = ?;"
    )
    params = (server, ram, cpu, disk, uptime)
    executeSQLQuery(query, params)