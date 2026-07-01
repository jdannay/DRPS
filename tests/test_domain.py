import unittest

from retirement.domain import Person


class PersonTest(unittest.TestCase):
    def test_age(self):
        self.assertEqual(Person("Jeff", 1960).age(2026), 66)
