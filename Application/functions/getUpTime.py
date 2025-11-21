import psutil
import datetime

def getUpTime():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    return str(uptime).split('.')[0]
