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

    def test_insert_all(self):
        self.db.create()
        self.db.insert_volume(10)
        self.db.insert_stream("abc")
        self.db.insert_pos_lang_mittel_kurz(21)
        self.db.insert_pos_ukw(22)
        self.db.insert_button_ukw(0)
        self.db.insert_button_lang(1)
        self.db.insert_butto_mittel(1)
        self.db.insert_button_kurz(0)
        self.db.insert_button_on_off(0)
        self.db.insert_button_spr_mus(0)



