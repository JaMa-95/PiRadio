import threading
from typing import List
from collections import deque

from Radio.util.singleton import Singleton


class SensorMsg:
    def __init__(self):
        self.buttons_data: ButtonsData = ButtonsData()
        self.analog_data: AnalogData = AnalogData()

    def set_buttons_data(self, data):
        self.buttons_data = data

    def __eq__(self, value: object) -> bool:
        if value is None:
            return False
        if self.buttons_data == value.buttons_data and self.analog_data == value.analog_data:
            return True
        return False

    def __str__(self):
        buttons_data_str = "\n".join([f"Pin: {button.pin}, State: {button.state}, States: {list(button.states)}" for button in self.buttons_data.get_data()])
        analog_data_str = "\n".join([f"Pin: {value.pin}, Value: {value.value}, Min: {value.min}, Max: {value.max}, Accepted Difference: {value.accepted_difference}" for value in self.analog_data.get_data_sensor()])
        return f"Buttons Data:\n{buttons_data_str}\n\nAnalog Data:\n{analog_data_str}"


class SensorData(Singleton):
    def __init__(self):
        self.buttons_data: ButtonsData = ButtonsData()
        self.analog_data: AnalogData = AnalogData()
        self.lock = threading.Lock()

    def set_buttons_data(self, data):
        with self.lock:
            self.buttons_data = data

    def set_analog_data(self, data):
        with self.lock:
            self.analog_data = data

    def set_data(self, sensor_msg: SensorMsg):
        with self.lock:
            self.buttons_data = sensor_msg.buttons_data
            self.analog_data = sensor_msg.analog_data


class SensorDataOld(SensorData):
    pass


class ButtonState:
    max_values = 20
    def __init__(self, pin: int, state: bool, states=None):
        if states is None:
            states = deque([False] * self.max_values)
        self.pin = pin
        self.state = state
        self.states = states

    def __eq__(self, other):
        if self.state == other.state and self.states == other.states:
            return True
        return False


class ButtonsData:
    def __init__(self):
        self.data: List[ButtonState] = []

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        data = other.get_data()
        if len(self.data) != len(data):
            return False
        for idx, value in enumerate(self.data):
            if value != data[idx]:
                return False
        return True
    
    def __str__(self):
        return "\n".join([f"Pin: {button.pin}, State: {button.state}, States: {list(button.states)}" for button in self.data])
        

    def is_empty(self):
        is_empty = not self.data
        return not is_empty

    def get_data(self) -> List[ButtonState]:
        return self.data

    def set_data(self, data: List[ButtonState]):
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
    def __init__(self, pin: int, value: int, min_: int, max_: int, accepted_difference: int = 8):
        self.pin: int = pin
        self.value: int = value
        self.min: int = min_
        self.max: int = max_
        self.accepted_difference: int = accepted_difference
        

class AnalogData:
    def __init__(self):
        self.sensor_data: List[AnalogValue] = []

    def __eq__(self, other):
        if other is None:
            return False
        sensor_data = other.get_data_sensor()
        if len(self.sensor_data) != len(sensor_data):
            return False
        for value in self.sensor_data:
            for value_other in sensor_data:
                if value.pin == value_other.pin:
                    if abs(value.value - value_other.value) > value.accepted_difference:
                        return False
        return True

    def __str__(self):
        return "\n".join([f"""Pin: {value.pin}, Value: {value.value}, Min: {value.min}, Max: {value.max}, 
                          Accepted Difference: {value.accepted_difference}""" for value in self.sensor_data])

    def is_empty(self) -> bool:
        return not self.sensor_data
    
    def delete_unchanged_values(self, other):
        other_sensor_data = other.get_data_sensor()
        values_to_remove = []
        for value in self.sensor_data:
            for value_other in other_sensor_data:
                if value.pin == value_other.pin:
                    if abs(value.value - value_other.value) <= value.accepted_difference:
                        values_to_remove.append(value)
        for value in values_to_remove:
            self.sensor_data.remove(value)

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