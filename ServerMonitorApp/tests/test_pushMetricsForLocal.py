import unittest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.pushMetricsForLocal import pushMetricsForLocal

class TestPushMetricsForLocal(unittest.TestCase):
    @patch('functions.pushMetricsForLocal.getRAMUsage', return_value=50.0)
    @patch('functions.pushMetricsForLocal.getDiskUsage', return_value=60.0)
    @patch('functions.pushMetricsForLocal.getCPUUsage', return_value=10.0)
    @patch('functions.pushMetricsForLocal.getUpTime', return_value="1 day, 0:00:00")
    @patch('functions.pushMetricsForLocal.getServicesWithStatus', return_value=[{'name': 'TestService', 'status': 'running'}])
    @patch('functions.pushMetricsForLocal.executeSQLQuery')
    @patch('functions.pushMetricsForLocal.platform')
    def test_pushMetricsForLocal_executes_queries(self, mock_platform, mock_executeSQLQuery, mock_getServicesWithStatus, mock_getUpTime, mock_getCPUUsage, mock_getDiskUsage, mock_getRAMUsage):
        """Test that pushMetricsForLocal calls executeSQLQuery for metrics and services."""
        mock_platform.node.return_value = "TestNode"
        pushMetricsForLocal()
        # Should call executeSQLQuery for metrics and for each service
        self.assertGreaterEqual(mock_executeSQLQuery.call_count, 2)
        # Check first call is for metrics
        args, kwargs = mock_executeSQLQuery.call_args_list[0]
        self.assertIn("@Server = ?, @RAMUsage = ?, @CPUusage = ?, @DiskUsage = ?, @Uptime = ?", args[0])
        # Check second call is for service
        args, kwargs = mock_executeSQLQuery.call_args_list[1]
        self.assertIn("@server = ?, @Service = ?, @Status = ?", args[0])

if __name__ == "__main__":
    unittest.main()