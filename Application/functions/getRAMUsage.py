import psutil
def getRAMUsage():
    return psutil.virtual_memory().percent
