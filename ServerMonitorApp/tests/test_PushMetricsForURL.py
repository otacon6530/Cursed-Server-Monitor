import unittest
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.pushMetricsForURL import pushMetricsForURL

class TestPushMetricsForURL(unittest.TestCase):
    @patch('functions.pushMetricsForURL.ping')
    @patch('functions.pushMetricsForURL.executeSQLQuery')
    def test_PushMetricsForURL_ping_true_executes_query(self, mock_executeSQLQuery, mock_ping):
        """Test that executeSQLQuery is called when ping returns True."""
        mock_ping.return_value = True
        pushMetricsForURL("testserver")
        mock_executeSQLQuery.assert_called_once()
        args, kwargs = mock_executeSQLQuery.call_args
        self.assertIn("EXECUTE [dbo].[SetServerMetrics]", args[0])
        self.assertEqual(args[1], ("testserver",))

    @patch('functions.pushMetricsForURL.ping')
    @patch('functions.pushMetricsForURL.executeSQLQuery')
    def test_PushMetricsForURL_ping_false_does_not_execute_query(self, mock_executeSQLQuery, mock_ping):
        """Test that executeSQLQuery is not called when ping returns False."""
        mock_ping.return_value = False
        pushMetricsForURL("testserver")
        mock_executeSQLQuery.assert_not_called()

if __name__ == "__main__":
    unittest.main()