import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.ping import ping

class TestPing(unittest.TestCase):
    def test_ping_success(self):
        """Test that ping returns True for a reachable host."""
        # 'localhost' should always be reachable
        self.assertTrue(ping('localhost'))

    def test_ping_failure(self):
        """Test that ping returns False for an unreachable host."""
        # 'invalid.host' should not be reachable
        self.assertFalse(ping('invalid.host'))

if __name__ == "__main__":
    unittest.main()