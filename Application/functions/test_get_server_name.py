import unittest
from functions.get_server_name import get_computer_name
import socket

class TestGetComputerName(unittest.TestCase):
    def test_computer_name(self):
        expected = socket.gethostname()
        actual = get_computer_name()
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()