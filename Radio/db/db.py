import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect("radio.db")
        self.cur = self.con.cursor()

    def create(self):
        self.cur.execute("CREATE TABLE buttonOnOff(value)")
        self.cur.execute("CREATE TABLE buttonLang(value)")
        self.cur.execute("CREATE TABLE buttonMittel(value)")
        self.cur.execute("CREATE TABLE buttonKurz(value)")
        self.cur.execute("CREATE TABLE buttonUKW(value)")
        self.cur.execute("CREATE TABLE buttonSprMus(value)")
        self.cur.execute("CREATE TABLE posLangMittelKurz(value)")
        self.cur.execute("CREATE TABLE posUKW(value)")
        self.cur.execute("CREATE TABLE volume(value)")

    def table_exists(self, table_name: str):
        res = self.cur.execute(f"SELECT name FROM sqlite_master WHERE name='{table_name}'")
        return res.fetchone() is not None

    def insert_button_on_off(self, value: int):
        self.cur.execute("INSERT INTO buttonOnOff VALUES(?)", (value,))
        self.con.commit()
        
    def insert_button_lang(self, value: int):
        self.cur.execute("INSERT INTO buttonLang VALUES(?)", (value,))
        self.con.commit()
        
    def insert_butto_mittel(self, value: int):
        self.cur.execute("INSERT INTO buttonMittel VALUES(?)", (value,))
        self.con.commit()
        
    def insert_button_kurz(self, value: int):
        self.cur.execute("INSERT INTO buttonKurz VALUES(?)", (value,))
        self.con.commit()
        
    def insert_button_ukw(self, value: int):
        self.cur.execute("INSERT INTO buttonUKW VALUES(?)", (value,))
        self.con.commit()
        
    def insert_button_spr_mus(self, value: int):
        self.cur.execute("INSERT INTO buttonSprMus VALUES(?)", (value,))
        self.con.commit()
        
    def insert_volume(self, value: int):
        self.cur.execute("INSERT INTO volume VALUES(?)", (value,))
        self.con.commit()
        
    def insert_pos_lang_mittel_kurz(self, value: int):
        self.cur.execute("INSERT INTO posLangMittelKurz VALUES(?)", (value,))
        self.con.commit()
        
    def insert_pos_ukw(self, value: int):
        self.cur.execute("INSERT INTO posUKW VALUES(?)", (value,))
        self.con.commit()

    #######################################################################

    def get_button_on_off(self):
        res = self.cur.execute("SELECT * FROM buttonOnOff ORDER BY value DESC LIMIT 1;")
        value = res.fetchall()
        return value[0]

    def get_button_lang(self):
        res = self.cur.execute("SELECT * FROM buttonLang ORDER BY value DESC LIMIT 1;")
        value = res.fetchall()
        return value[0]

    def get_button_mittel(self):
        res = self.cur.execute("SELECT * FROM buttonMittel ORDER BY value DESC LIMIT 1;")
        value = res.fetchall()
        return value[0]

    def get_button_kurz(self):
        res = self.cur.execute("SELECT * FROM buttonKurz ORDER BY value DESC LIMIT 1;")
        value = res.fetchall()
        return value[0]

    def get_button_ukw(self):
        res = self.cur.execute("SELECT * FROM buttonUKW ORDER BY value DESC LIMIT 1;")
        value = res.fetchall()
        return value[0]

    def get_button_spr_mus(self):
        res = self.cur.execute("SELECT * FROM buttonSprMus ORDER BY value DESC LIMIT 1;")
        value = res.fetchall()
        return value[0]

    def get_volume(self):
        res = self.cur.execute("SELECT * FROM volume ORDER BY value DESC LIMIT 1;")
        value = res.fetchall()
        return value[0]

    def get_pos_lang_mittel_kurz(self):
        res = self.cur.execute("SELECT * FROM posLangMittelKurz ORDER BY value DESC LIMIT 1;")
        value = res.fetchall()
        return value

    def get_pos_ukw(self):
        res = self.cur.execute("SELECT * FROM posUKW ORDER BY value DESC LIMIT 1;")
        value = res.fetchall()
        return value

