import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.getCPUUsage import getCPUUsage

class TestGetCPUUsage(unittest.TestCase):
    def test_getCPUUsage_returns_float(self):
        usage = getCPUUsage()
        self.assertIsInstance(usage, float)

    def test_getCPUUsage_range(self):
        usage = getCPUUsage()
        self.assertGreaterEqual(usage, 0.0)
        self.assertLessEqual(usage, 100.0)

if __name__ == "__main__":
    unittest.main()
