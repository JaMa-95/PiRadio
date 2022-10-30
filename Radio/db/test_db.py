from db import Database
from unittest import TestCase


class TestDb(TestCase):
    def setUp(self) -> None:
        self.db = Database()

    def test_create(self):
        self.db.create()

    def test_get(self):
        self.db.replace_volume(10)
        value = self.db.get_volume()
        self.assertEqual(value, 10)

    def test_init(self):
        self.db.create()
        self.db.init()

    def test_(self):
        abc = self.db.cur.execute("PRAGMA index_list('radio');")
        d = abc.fetchall()
        print()

    def test_replace_all(self):
        self.db.replace_volume(2)
        self.db.replace_stream("def")
        self.db.replace_pos_lang_mittel_kurz(2)
        self.db.replace_pos_ukw(2)
        self.db.replace_button_ukw(2)
        self.db.replace_button_lang(2)
        self.db.replace_button_mittel(2)
        self.db.replace_button_kurz(2)
        self.db.replace_button_on_off(2)
        self.db.replace_button_spr_mus(2)

    def test_multiple(self):
        for _ in range(100):
            self.db.insert_volume(1)
            self.db.insert_stream("asd")
            self.db.insert_pos_lang_mittel_kurz(2)
            self.db.insert_pos_ukw(2)
            self.db.insert_button_ukw(2)
            self.db.insert_button_lang(2)
            self.db.insert_button_mittel(2)
            self.db.insert_button_kurz(2)
            self.db.insert_button_on_off(2)
            self.db.insert_button_spr_mus(2)

    def test_clear_db(self):
        self.db.clear()



