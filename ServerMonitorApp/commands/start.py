from datetime import datetime, timedelta
import click
from functions.pushMetricsForURL import pushMetricsForURL
from functions.pushMetricsForLocal import pushMetricsForLocal
from functions.pushServicesForLocal import pushServicesForLocal
import time
import threading

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
            if metrics_thread is None or not metrics_thread.is_alive():
                metrics_thread = threading.Thread(target=pushMetricsForURL, args=(url,))
                metrics_thread.start()
        else:
            if metrics_thread is None or not metrics_thread.is_alive():
                metrics_thread = threading.Thread(target=pushMetricsForLocal)
                metrics_thread.start()

            if services_thread is None or not services_thread.is_alive():
                services_thread = threading.Thread(target=pushServicesForLocal)
                services_thread.start()
        while datetime.now() < future_time:
            time.sleep(1)
