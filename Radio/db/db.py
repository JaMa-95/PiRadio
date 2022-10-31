import sqlite3
import threading
import time


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

    """
    def create(self):
        for value in ["buttonOnOff", "buttonLang", "buttonMittel", "buttonKurz", "buttonUKW", "buttonSprMus",
                      "posLangMittelKurz", "posLangMittelKurz", "posUKW", "volume", "stream"]:
            try:
                self.cur.execute(f"CREATE TABLE {value}(time, value)")
            except sqlite3.OperationalError:
                self.cur.execute(f'DELETE FROM {value};', )
    """

    def create(self):
        try:
            self.cur.execute(f"CREATE TABLE radio(name, value)")
            self.cur.execute("CREATE UNIQUE INDEX idx ON contacts (name);")
        except sqlite3.OperationalError:
            pass

    def clear(self):
        for value in ["buttonOnOff", "buttonLang", "buttonMittel", "buttonKurz", "buttonUKW", "buttonSprMus",
                      "posLangMittelKurz", "posLangMittelKurz", "posUKW", "volume", "stream"]:
            self.cur.execute(
                f'DELETE from {value}  sqlite_master order by time desc limit 1);'
            )

    def init(self):
        self.insert_volume(0)
        self.insert_stream("INITIALIZING")
        self.insert_pos_lang_mittel_kurz(0)
        self.insert_pos_ukw(0)
        self.insert_button_ukw(0)
        self.insert_button_lang(0)
        self.insert_button_mittel(0)
        self.insert_button_kurz(0)
        self.insert_button_on_off(0)
        self.insert_button_spr_mus(0)

    def table_exists(self, table_name: str):
        with self.lock:
            res = self.cur.execute(f"SELECT * FROM radio WHERE name='{table_name}'")
            return res.fetchone() is not None

    ###################################################################################

    def replace_stream(self, value: str):
        with self.lock:
            self.cur.execute("""UPDATE radio SET value = ? WHERE name=?""", (value, "stream"))
            self.con.commit()

    def replace_button_on_off(self, value: int):
        with self.lock:
            self.cur.execute(f"UPDATE radio SET value = {value} WHERE name='buttonOnOff'")
            self.con.commit()

    def replace_button_lang(self, value: int):
        print(f"REPLACE LANG: {value}")
        with self.lock:
            self.cur.execute(f"UPDATE radio SET value = {value} WHERE name='buttonLang'")
            self.con.commit()

    def replace_button_mittel(self, value: int):
        with self.lock:
            self.cur.execute(f"UPDATE radio SET value = {value} WHERE name='buttonMittel'")
            self.con.commit()

    def replace_button_kurz(self, value: int):
        with self.lock:
            self.cur.execute(f"UPDATE radio SET value = {value} WHERE name='buttonKurz'")
            self.con.commit()

    def replace_button_ukw(self, value: int):
        with self.lock:
            self.cur.execute(f"UPDATE radio SET value = {value} WHERE name='buttonUKW'")
            self.con.commit()

    def replace_button_spr_mus(self, value: int):
        with self.lock:
            self.cur.execute(f"UPDATE radio SET value = {value} WHERE name='buttonSprMus'")
            self.con.commit()

    def replace_volume(self, value: int):
        with self.lock:
            self.cur.execute(f"UPDATE radio SET value = {value} WHERE name='volume'")
            self.con.commit()

    def replace_pos_lang_mittel_kurz(self, value: int):
        with self.lock:
            self.cur.execute(f"UPDATE radio SET value = {value} WHERE name='posLangMittelKurz'")
            self.con.commit()

    def replace_pos_ukw(self, value: int):
        with self.lock:
            self.cur.execute(f"UPDATE radio SET value = {value} WHERE name='posUKW'")
            self.con.commit()

    #########################################################################################

    def insert_stream(self, value: str):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("stream", value))
            self.con.commit()

    def insert_button_on_off(self, value: int):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("buttonOnOff", value))
            self.con.commit()

    def insert_button_lang(self, value: int):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("buttonLang", value))
            self.con.commit()

    def insert_button_mittel(self, value: int):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("buttonMittel", value))
            self.con.commit()

    def insert_button_kurz(self, value: int):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("buttonKurz", value))
            self.con.commit()

    def insert_button_ukw(self, value: int):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("buttonUKW", value))
            self.con.commit()

    def insert_button_spr_mus(self, value: int):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("buttonSprMus", value))
            self.con.commit()

    def insert_volume(self, value: int):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("volume", value))
            self.con.commit()

    def insert_pos_lang_mittel_kurz(self, value: int):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("posLangMittelKurz", value))
            self.con.commit()

    def insert_pos_ukw(self, value: int):
        with self.lock:
            self.cur.execute("REPLACE INTO radio VALUES(?, ?)", ("posUKW", value))
            self.con.commit()

    #######################################################################

    def get_stream(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='stream'")
            value = res.fetchall()
            return value[0][1]

    def get_button_on_off(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonOnOff'")
            value = res.fetchall()
            return value[0][1]

    def get_button_on_off_web(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonOnOff'")
            value = res.fetchall()
            if value[0][1] > 50:
                return "Off"
            return "On"

    def get_button_lang(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonLang'")
            value = res.fetchall()
            return value[0][1]

    def get_button_lang_web(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonLang'")
            value = res.fetchall()
            print(f"BUTTON LANG: {value[0][1]}")
            if value[0][1] > 50:
                return "Off"
            return "On"

    def get_button_mittel(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonMittel'")
            value = res.fetchall()
            return value[0][1]

    def get_button_mittel_web(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonMittel'")
            value = res.fetchall()
            if value[0][1] > 50:
                return "Off"
            return "On"

    def get_button_kurz(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonKurz'")
            value = res.fetchall()
            return value[0][1]

    def get_button_kurz_web(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonKurz'")
            value = res.fetchall()
            if value[0][1] > 50:
                return "Off"
            return "On"

    def get_button_ukw(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonUKW'")
            value = res.fetchall()
            return value[0][1]

    def get_button_ukw_web(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonUKW'")
            value = res.fetchall()
            if value[0][1] > 50:
                return "Off"
            return "On"

    def get_button_spr_mus(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='volume'")
            value = res.fetchall()
            return value[0][1]

    def get_button_spr_mus_web(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='buttonSprMus'")
            value = res.fetchall()
            if value[0][1] > 50:
                return "Off"
            return "On"

    def get_volume(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='volume'")
            value = res.fetchall()
            return value[0][1]

    def get_pos_lang_mittel_kurz(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='posLangMittelKurz'")
            value = res.fetchall()
            return value[0][1]

    def get_pos_ukw(self):
        with self.lock:
            res = self.cur.execute("SELECT * FROM radio WHERE name='posUKW'")  #
            value = res.fetchall()
            return value[0][1]
