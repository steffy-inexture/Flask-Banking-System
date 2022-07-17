import unittest
from banking_system.users.routes import add

class User(unittest.TestCase):
    pass

class UserRoutes(unittest.TestCase):
    pass

class UserForms(unittest.TestCase):
    pass

class AdminRoutes(unittest.TestCase):
    pass

class AdminForms(unittest.TestCase):
    pass

class TestCalc(unittest.TestCase):

    def test_add(self):
        result = add(10, 5)
        self.assertEqual(result, 15)