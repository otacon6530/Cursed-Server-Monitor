import psutil

def getDiskUsage():
    return psutil.disk_usage('/').percent
