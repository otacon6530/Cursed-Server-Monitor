
import click
import time

from datetime import datetime, timedelta

from functions.pushMetricsForURL import pushMetricsForURL
from functions.pushMetricsForLocal import pushMetricsForLocal
from functions.pushServicesForLocal import pushServicesForLocal
from functions.startThread import startThread

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
            metrics_thread = startThread(metrics_thread, pushMetricsForURL, (url,))
        else:
            metrics_thread = startThread(metrics_thread, pushMetricsForLocal)
            services_thread = startThread(services_thread, pushServicesForLocal)

        while datetime.now() < future_time:
            time.sleep(1)
