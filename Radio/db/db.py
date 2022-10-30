import sqlite3
import threading


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                # another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class Database(Singleton):
    def __init__(self):
        self.con = sqlite3.connect("radio.db",
                                   check_same_thread=False)
        self.cur = self.con.cursor()

        self.lock = threading.Lock()

    def create(self):
        for value in ["buttonOnOff", "buttonLang", "buttonMittel", "buttonKurz", "buttonUKW", "buttonSprMus",
                      "posLangMittelKurz", "posLangMittelKurz", "posUKW", "volume", "stream"]:
            try:
                self.cur.execute(f"CREATE TABLE {value}(value)")
            except sqlite3.OperationalError:
                pass

    def test_data(self):
        self.insert_volume(10)
        self.insert_stream("abc")
        self.insert_pos_lang_mittel_kurz(21)
        self.insert_pos_ukw(22)
        self.insert_button_ukw(0)
        self.insert_button_lang(1)
        self.insert_butto_mittel(1)
        self.insert_button_kurz(0)
        self.insert_button_on_off(0)
        self.insert_button_spr_mus(0)

    def table_exists(self, table_name: str):
        try:
            self.lock.acquire(True)
            res = self.cur.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'")
            return res.fetchone() is not None
        finally:
            self.lock.release()

    def insert_stream(self, value: str):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO stream VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    def insert_button_on_off(self, value: int):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO buttonOnOff VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    def insert_button_lang(self, value: int):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO buttonLang VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    def insert_butto_mittel(self, value: int):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO buttonMittel VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    def insert_button_kurz(self, value: int):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO buttonKurz VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    def insert_button_ukw(self, value: int):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO buttonUKW VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    def insert_button_spr_mus(self, value: int):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO buttonSprMus VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    def insert_volume(self, value: int):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO volume VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    def insert_pos_lang_mittel_kurz(self, value: int):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO posLangMittelKurz VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    def insert_pos_ukw(self, value: int):
        try:
            self.lock.acquire(True)
            self.cur.execute("INSERT INTO posUKW VALUES(?)", (value,))
            self.con.commit()
        finally:
            self.lock.release()

    #######################################################################

    def get_stream(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM stream ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()

    def get_button_on_off(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonOnOff ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()

    def get_button_on_off_web(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonOnOff ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            if value[0][0] == 0:
                return "Off"
            return "On"
        finally:
            self.lock.release()

    def get_button_lang(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonLang ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()

    def get_button_lang_web(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonLang ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            if value[0][0] == 0:
                return "Off"
            return "On"
        finally:
            self.lock.release()

    def get_button_mittel(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonMittel ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()

    def get_button_mittel_web(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonMittel ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            if value[0][0] == 0:
                return "Off"
            return "On"
        finally:
            self.lock.release()

    def get_button_kurz(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonKurz ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()

    def get_button_kurz_web(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonKurz ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            if value[0][0] == 0:
                return "Off"
            return "On"
        finally:
            self.lock.release()

    def get_button_ukw(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonUKW ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()

    def get_button_ukw_web(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonUKW ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            if value[0][0] == 0:
                return "Off"
            return "On"
        finally:
            self.lock.release()

    def get_button_spr_mus(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonSprMus ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()

    def get_button_spr_mus_web(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM buttonSprMus ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            if value[0][0] == 0:
                return "Off"
            return "On"
        finally:
            self.lock.release()

    def get_volume(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM volume ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()

    def get_pos_lang_mittel_kurz(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM posLangMittelKurz ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()

    def get_pos_ukw(self):
        try:
            self.lock.acquire(True)
            res = self.cur.execute("SELECT * FROM posUKW ORDER BY value DESC LIMIT 1;")
            value = res.fetchall()
            return value[0][0]
        finally:
            self.lock.release()
