from db import Database
from unittest import TestCase


class TestDb(TestCase):
    def setUp(self) -> None:
        self.db = Database()

    def test_create(self):
        self.db.create()

    def test_insert_get(self):
        self.db.insert_volume(10)
        value = self.db.get_volume()
        self.assertEqual(value, 10)



