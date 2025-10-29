import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.getServicesWithStatus import getServicesWithStatus

class TestGetServicesWithStatus(unittest.TestCase):
    def test_returns_list(self):
        """Test that getServicesWithStatus returns a list."""
        result = getServicesWithStatus()
        self.assertIsInstance(result, list)

    def test_dict_structure(self):
        """Test that each item in the result is a dict with 'name' and 'status' keys."""
        result = getServicesWithStatus()
        for service in result:
            self.assertIsInstance(service, dict)
            self.assertIn('name', service)
            self.assertIn('status', service)

    def test_exception_handling(self):
        """Test that an exception is handled gracefully."""
        # Simulate unsupported platform by patching platform.system
        import platform
        original_system = platform.system
        platform.system = lambda: "unsupported"
        result = getServicesWithStatus()
        platform.system = original_system
        self.assertEqual(result[0]['name'], '[EXCEPTION]')

if __name__ == "__main__":
    unittest.main()