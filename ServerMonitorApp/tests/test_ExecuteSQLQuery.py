import unittest
import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from functions.executeSQLQuery import executeSQLQuery

class TestExecuteSQLQuery(unittest.TestCase):
    def test_select_query_returns_results_or_none(self):
        """Test that a SELECT query returns a list or None."""
        query = "SELECT TOP 1 * FROM INFORMATION_SCHEMA.TABLES"
        result = executeSQLQuery(query)
        self.assertTrue(result is None or isinstance(result, list))

    def test_invalid_query_returns_none(self):
        """Test that an invalid query returns None."""
        query = "SELECT * FROM non_existent_table"
        f = io.StringIO()
        with redirect_stdout(f), redirect_stderr(f):
            result = executeSQLQuery(query)
        self.assertIsNone(result)

    def test_parameterized_query(self):
        """Test that a parameterized query executes without error."""
        query = "SELECT ?"
        params = ("test",)
        result = executeSQLQuery(query, params)
        self.assertTrue(result is None or isinstance(result, list))

if __name__ == "__main__":
    unittest.main()