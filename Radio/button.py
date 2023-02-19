import datetime
from dataclasses import dataclass
import RPi.GPIO as GPIO


class ButtonESP:
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
        if self.last_click[0] and self.last_click[1]:
            time_delta_a = self.last_click[0] - self.last_click[1]
            time_delta_b = self.last_click[1] - self.last_click[0]
            if time_delta_a.seconds < 2 or time_delta_b.seconds < 2:
                self.reset_double_click()
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
        self.last_click[self.get_last_clicked_index()] = datetime.datetime.now()


@dataclass
class RadioButtonsESP:
    button_on_off: ButtonESP = ButtonESP()
    button_lang: ButtonESP = ButtonESP()
    button_mittel: ButtonESP = ButtonESP()
    button_kurz: ButtonESP = ButtonESP()
    button_ukw: ButtonESP = ButtonESP()
    button_spr: ButtonESP = ButtonESP()


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

class ButtonRaspi:
    def __init__(self, button_number: int = 0, long_click_threshold: int = 50):
        # BCM-Nummerierung verwenden
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_number, GPIO.OUT)
        self.button_number = button_number
        self.value: int = 99
        self.value_old: int = None
        self.value_olds = []
        self.value_old_index = 0
        self.indexer = 0

        self.long_threshold: int = long_click_threshold

        self.last_click: list = [None, None]
        self.last_click_index: int = 0

        self.is_clicked: bool = False
        self.on_off_wait: bool = False

        self.state = False

    def is_click(self):
        # TODO: check if indexer needed
        if not self.on_off_wait and self.indexer > 5:
            self.on_off_wait = True
            self.state = GPIO.input(self.button_number)
            self.set_is_clicked()
            return True
        return False

    def double_click(self):
        if self.last_click[0] and self.last_click[1]:
            time_delta_a = self.last_click[0] - self.last_click[1]
            time_delta_b = self.last_click[1] - self.last_click[0]
            if time_delta_a.seconds < 2 or time_delta_b.seconds < 2:
                self.reset_double_click()
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

    def set_value(self):
        """
        :return: True if changed
        """
        state = GPIO.input(self.button_number)
        self.value_olds.append(state)
        self.value_old = self.value
        self.value = state
        if state:
            self.is_clicked = True
            self.indexer += 1
            return True
        else:
            self.on_off_wait = False
            self.is_clicked = False
            self.indexer = 0
            return True

    def get_last_clicked_index(self):
        self.last_click_index = (self.last_click_index + 1) % 2
        return self.last_click_index

    def set_is_clicked(self):
        self.last_click[self.get_last_clicked_index()] = datetime.datetime.now()


@dataclass
class RadioButtonsRaspi:
    button_on_off: ButtonRaspi = ButtonRaspi(23)
    button_lang: ButtonRaspi = ButtonRaspi(24)
    button_mittel: ButtonRaspi = ButtonRaspi(25)
    button_kurz: ButtonRaspi = ButtonRaspi(8)
    button_ukw: ButtonRaspi = ButtonRaspi(7)
    button_spr: ButtonRaspi = ButtonRaspi(12)

    def set_value(self):
        self.button_on_off.set_value()
        self.button_lang.set_value()
        self.button_mittel.set_value()
        self.button_kurz.set_value()
        self.button_ukw.set_value()
        self.button_spr.set_value()
        return True

    def get_pressed_button(self):
        self.set_value()
        state_on = self.button_on_off.state
        if state_on:
            state = self.button_lang.state
            if state:
                return "buttonLang"
            state = self.button_mittel.state
            if state:
                return "buttonMittel"
            state = self.button_kurz.state
            if state:
                return "buttonKurz"
            state = self.button_ukw.state
            if state:
                return "buttonUKW"
            state = self.button_spr.state
            if state:
                return "buttonSprMus"

