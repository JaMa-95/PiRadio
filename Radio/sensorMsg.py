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

    def update_value(self, pin, value_new: ButtonState) -> bool:
        for idx, value in enumerate(self.data):
            if value.pin == pin:
                self.data[idx] = value_new
                return True
        return False

    def get_value(self, pin) -> ButtonState:
        for idx, value in enumerate(self.data):
            if value.pin == pin:
                return value


class AnalogValue:
    def __init__(self, pin: int, value: int):
        self.pin: int = pin
        self.value: int = value
        

class AnalogData:
    def __init__(self):
        self.sensor_data: List[AnalogValue] = []

    def is_empty(self) -> bool:
        return not self.sensor_data

    def get_data_sensor(self) -> List[AnalogValue]:
        return self.sensor_data

    def set_data(self, list_of_analog_value: List[AnalogValue]):
        self.sensor_data = list_of_analog_value

    def add_value(self, value: AnalogValue):
        self.sensor_data.append(value)

    def delete_value(self, pin) -> bool:
        for value in self.sensor_data:
            if value.pin == pin:
                self.sensor_data.remove(value)
                return True
        return False
