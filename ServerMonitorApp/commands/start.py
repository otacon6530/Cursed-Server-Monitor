from datetime import datetime, timedelta
import click
from functions.pushMetricsForURL import pushMetricsForURL
from functions.pushMetricsForLocal import pushMetricsForLocal
from functions.pushServicesForLocal import pushServicesForLocal
import time
import threading

def start_thread_if_needed(thread, target, args=None):
    if thread is None or not thread.is_alive():
        if args:
            thread = threading.Thread(target=target, args=args)
        else:
            thread = threading.Thread(target=target)
        thread.start()
    return thread

@click.command()
@click.argument("url", required=False)
def start(url):
    """Starts the service to push client metrics to the central hub."""
    print("Service Started")
    services_thread = None
    metrics_thread = None

    while True:
        future_time = datetime.now() + timedelta(seconds=5)
        if url:
            metrics_thread = start_thread_if_needed(metrics_thread, pushMetricsForURL, (url,))
        else:
            metrics_thread = start_thread_if_needed(metrics_thread, pushMetricsForLocal)
            services_thread = start_thread_if_needed(services_thread, pushServicesForLocal)

        while datetime.now() < future_time:
            time.sleep(1)
