from typing import List


class SensorMsg:
    def __init__(self):
        self.buttons_data: ButtonsData = ButtonsData()
        self.analog_data: AnalogData = AnalogData()


class ButtonState:
    def __init__(self, pin: int, state: bool, states: []):
        self.pin = pin
        self.state = state
        self.states = states


class ButtonsData:
    def __init__(self):
        self.data: List[ButtonState] = []

    def is_empty(self):
        is_empty = not self.data
        return not is_empty

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def add_value(self, value: ButtonState):
        self.data.append(value)

    def delete_value(self, pin) -> bool:
        for value in self.data:
            if value.pin == pin:
                self.data.remove(value)
                return True
        return False


class AnalogValue:
    def __init__(self, pin: int, value: int):
        self.pin = pin
        self.value = value


class AnalogData:
    def __init__(self):
        self.data: List[AnalogValue] = []

    def is_empty(self):
        is_empty = not self.data
        return not is_empty

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def add_value(self, value: AnalogValue):
        self.data.append(value)

    def delete_value(self, pin) -> bool:
        for value in self.data:
            if value.pin == pin:
                self.data.remove(value)
                return True
        return False
