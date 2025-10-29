from datetime import datetime, timedelta
import click
from functions.pushMetricsForURL import pushMetricsForURL
from functions.pushMetricsForLocal import pushMetricsForLocal
from functions.pushServicesForLocal import pushServicesForLocal
import time

@click.command()
@click.argument("url", required=False)
def start(url):
    """Starts the service to push client metrics to the central hub."""
    print("Service Started")
    while True:
        future_time = datetime.now() + timedelta(seconds=5)
        if url:
            pushMetricsForURL(url)
        else:
            pushMetricsForLocal()
            pushServicesForLocal()
        while datetime.now() < future_time:
            time.sleep(1)
