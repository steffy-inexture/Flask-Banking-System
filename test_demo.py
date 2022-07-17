import unittest
from banking_system.users.routes import add

class TestCalc(unittest.TestCase):

    def test_add(self):
        result = add(10, 5)
        self.assertEqual(result, 15)
