import click
import unittest

from functions.getRAMUsage import getRAMUsage
from functions.getDiskUsage import getDiskUsage
from functions.getCPUUsage import getCPUUsage
from functions.getUpTime import getUpTime
from functions.ping import ping
from functions.getServicesWithStatus import getServicesWithStatus

from tests.test_GetCPUUsage import TestGetCPUUsage
from tests.test_GetDiskUsage import TestGetDiskUsage
from tests.test_GetRAMUsage import TestGetRAMUsage
from tests.test_GetUpTime import TestGetUpTime
from tests.test_ping import TestPing
from tests.test_GetServicesWithStatus import TestGetServicesWithStatus
from tests.test_ExecuteSQLQuery import TestExecuteSQLQuery
from tests.test_PushMetricsForURL import TestPushMetricsForURL
from tests.test_pushMetricsForLocal import TestPushMetricsForLocal
from tests.test_pushServicesForLocal import TestPushServicesForLocal

@click.command()
def test():
    """Display system metrics (uptime, CPU, RAM, disk usage), ping a remote host, list all services and their status, and run all unit tests for core functions."""
    print(f"Uptime: {getUpTime()}")
    print(f"CPU Usage: {getCPUUsage()}")
    print(f"RAM Usage: {getRAMUsage()}")
    print(f"Disk Usage: {getDiskUsage()}")
    print(f"Ping: {ping('home.stephensdev.com')}")
    services = getServicesWithStatus()
    print(f"Services:")
    for service in services:
        if service['name'] == '[EXCEPTION]':
            continue
        print(f"{service['name']}: {service['status']}")

    # Run unit tests after prints
    print("\nRunning unit tests...")
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGetCPUUsage))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGetDiskUsage))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGetRAMUsage))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGetUpTime))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPing))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGetServicesWithStatus))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestExecuteSQLQuery))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPushMetricsForURL))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPushMetricsForLocal))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPushServicesForLocal))
    runner = unittest.TextTestRunner()
    runner.run(suite)