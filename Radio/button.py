import datetime
from dataclasses import dataclass


class Button:
    def __init__(self, click_threshold: int = 30, long_click_threshold: int = 50):
        self.value: int = 99
        self.value_old: int = None
        self.value_olds = []
        self.value_old_index = 0
        self.threshold: int = click_threshold
        self.long_threshold: int = long_click_threshold
        self.indexer = 0

        self.last_click: list = [None, None]
        self.last_click_index: int = 0

        self.is_clicked: bool = False
        self.on_off_wait: bool = False

        self.state = False

    def is_click(self):
        if self.value < self.threshold and self.indexer > 5 and not self.on_off_wait:
            self.on_off_wait = True
            self.state = not self.state
            self.set_is_clicked()
            return True
        return False

    def double_click(self):
        time_delta_a = self.last_click[0] - self.last_click[1]
        time_delta_b = self.last_click[1] - self.last_click[0]
        print(f"lAST CLICK 0: {self.last_click[0]}")
        print(f"lAST CLICK 1: {self.last_click[1]}")
        if time_delta_a.seconds < 4 or time_delta_b.seconds < 4:
            return True
        return False

    def reset_double_click(self):
        self.last_click[0] = None
        self.last_click[1] = None

    def long_click(self):
        if self.indexer > self.long_threshold:
            return True
        return False

    def get_value(self):
        return self.value

    def set_value(self, value: int):
        """

        :param value:
        :return: True if changed
        """
        self.value_olds.append(value)
        self.value_old = self.value
        self.value = value
        if value < self.threshold:
            self.is_clicked = True
            self.indexer += 1
            if (value / self.value_old) < 0.5 and self.value_old > 30:
                return True
        else:
            self.on_off_wait = False
            self.is_clicked = False
            self.indexer = 0
            if self.value_old < self.threshold:
                return True
        return False

    def get_last_clicked_index(self):
        self.last_click_index = (self.last_click_index + 1) % 2
        return self.last_click_index

    def set_is_clicked(self):
        if self.is_clicked and not self.value:
            self.last_click[self.get_last_clicked_index()] = datetime.datetime.now()


@dataclass
class RadioButtons:
    button_on_off: Button = Button()
    button_lang: Button = Button()
    button_mittel: Button = Button()
    button_kurz: Button = Button()
    button_ukw: Button = Button()
    button_spr: Button = Button()

    def set_value(self, name: str, value: int):
        if name == "buttonOnOff":
            return self.button_on_off.set_value(value)
        elif name == "buttonLang":
            return self.button_lang.set_value(value)
        elif name == "buttonMittel":
            return self.button_mittel.set_value(value)
        elif name == "buttonKurz":
            return self.button_kurz.set_value(value)
        elif name == "buttonUKW":
            return self.button_ukw.set_value(value)
        elif name == "buttonSprMus":
            return self.button_spr.set_value(value)

    def get_pressed_button(self):
        if self.button_lang.is_click():
            return
        for button, value in self.current_command.items():
            if value < self.button_threshold and button != "buttonOnOff":
                return button
            elif button == "posLangKurzMittel":
                # reached end of buttons
                return None
