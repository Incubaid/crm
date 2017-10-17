"""
Tests for home module
"""
import unittest
from tests.base_tests import BaseTestCase

class HomeTest(BaseTestCase):
    """
    Test for home module
    """
    def test_home(self):
        """
        Test home page
        """
        rv = self.app.get('/')
        assert rv.status_code == 200
        assert b'Quick links' in rv.data


if __name__ == '__main__':
    unittest.main()