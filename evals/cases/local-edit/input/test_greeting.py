import unittest
from greeting import greeting

class GreetingTests(unittest.TestCase):
    def test_named(self):
        self.assertEqual(greeting("Ada"), "Hello, Ada!")

    def test_empty(self):
        self.assertEqual(greeting(""), "Hello, guest!")
