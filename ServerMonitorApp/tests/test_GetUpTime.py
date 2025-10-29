import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.getUpTime import getUpTime

class TestGetUpTime(unittest.TestCase):
    def test_getUpTime_returns_string(self):
        """Test that getUpTime returns a string value."""
        uptime = getUpTime()
        self.assertIsInstance(uptime, str)

    def test_getUpTime_format(self):
        """Test that getUpTime returns a string in the expected format (contains days/hours/minutes/seconds)."""
        uptime = getUpTime()
        # Example format: '5 days, 9:32:25' or '0:32:25'
        self.assertRegex(uptime, r'(\d+ days, )?\d{1,2}:\d{2}:\d{2}')

if __name__ == "__main__":
    unittest.main()
