import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.getRAMUsage import getRAMUsage

class TestGetRAMUsage(unittest.TestCase):
    def test_getRAMUsage_returns_float(self):
        """Test that getRAMUsage returns a float value."""
        usage = getRAMUsage()
        self.assertIsInstance(usage, float)

    def test_getRAMUsage_range(self):
        """Test that getRAMUsage returns a value between 0 and 100."""
        usage = getRAMUsage()
        self.assertGreaterEqual(usage, 0.0)
        self.assertLessEqual(usage, 100.0)

if __name__ == "__main__":
    unittest.main()
