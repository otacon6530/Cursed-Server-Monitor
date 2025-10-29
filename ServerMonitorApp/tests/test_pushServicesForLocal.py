import unittest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.pushServicesForLocal import pushServicesForLocal

class TestPushServicesForLocal(unittest.TestCase):
    @patch('functions.pushServicesForLocal.getServicesWithStatus', return_value=[{'name': 'TestService', 'status': 'running'}])
    @patch('functions.pushServicesForLocal.executeSQLQuery')
    @patch('functions.pushServicesForLocal.platform')
    def test_pushServicesForLocal_executes_service_query(
        self,
        mock_platform,
        mock_executeSQLQuery,
        mock_getServicesWithStatus
    ):
        """Test that pushServicesForLocal calls executeSQLQuery for each service."""
        mock_platform.node.return_value = "TestNode"
        pushServicesForLocal()
        mock_executeSQLQuery.assert_called_once()
        args, kwargs = mock_executeSQLQuery.call_args
        self.assertIn("@server = ?, @Service = ?, @Status = ?", args[0])
        self.assertEqual(args[1], ("TestNode", "TestService", "running"))

    @patch('functions.pushServicesForLocal.getServicesWithStatus', return_value=[{'name': '[EXCEPTION]', 'status': 'error'}])
    @patch('functions.pushServicesForLocal.executeSQLQuery')
    @patch('functions.pushServicesForLocal.platform')
    def test_pushServicesForLocal_skips_exception_service(
        self,
        mock_platform,
        mock_executeSQLQuery,
        mock_getServicesWithStatus
    ):
        """Test that pushServicesForLocal skips services with name '[EXCEPTION]'."""
        mock_platform.node.return_value = "TestNode"
        pushServicesForLocal()
        mock_executeSQLQuery.assert_not_called()

if __name__ == "__main__":
    unittest.main()