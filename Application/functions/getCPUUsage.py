import psutil

psutil.cpu_percent(interval=None, percpu=True)

def getCPUUsage():
    cpu_usages = psutil.cpu_percent(interval=1, percpu=True)
    average_usage = sum(cpu_usages) / len(cpu_usages)
    return round(average_usage, 1)
