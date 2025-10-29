import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.getDiskUsage import getDiskUsage

class TestGetDiskUsage(unittest.TestCase):
    def test_getDiskUsage_returns_float(self):
        """Test that getDiskUsage returns a float value."""
        usage = getDiskUsage()
        self.assertIsInstance(usage, float)

    def test_getDiskUsage_range(self):
        """Test that getDiskUsage returns a value between 0 and 100."""
        usage = getDiskUsage()
        self.assertGreaterEqual(usage, 0.0)
        self.assertLessEqual(usage, 100.0)

if __name__ == "__main__":
    unittest.main()