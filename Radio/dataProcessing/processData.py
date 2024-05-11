from Radio.dataProcessing.states import ButtonClickStates
from Radio.dataProcessing.radioFrequency import Frequencies, RadioFrequency
from Radio.util.sensorMsg import AnalogData, ButtonState, SensorMsg


class ButtonProcessData:
    def __init__(self, name: str, pin: int, frequency_list: Frequencies):
        self.name = name
        self.pin = pin
        self.state: ButtonState = ButtonState(pin=self.pin, state=False, states=[])
        self.short_threshold: int = 2
        self.long_threshold: int = 10
        self.radio_action = None
        self.frequency_list: Frequencies = frequency_list

    def set_radio_action(self, action):
        self.radio_action = action

    def process_data(self, sensor_msg_new: SensorMsg, sensor_msg_old: SensorMsg) -> SensorMsg:
        if self.state.state:
            sensor_msg_updated = self.radio_action.check_and_execute(ButtonClickStates.BUTTON_STATE_ON,
                                                                     sensor_msg_new,
                                                                     sensor_msg_old)
        else:
            sensor_msg_updated = self.radio_action.check_and_execute(ButtonClickStates.BUTTON_STATE_OFF,
                                                                     sensor_msg_new,
                                                                     sensor_msg_old)
        if self.is_short_click():
            return self.radio_action.check_and_execute(ButtonClickStates.BUTTON_STATE_SHORT_CLICK,
                                                       sensor_msg_updated,
                                                       sensor_msg_old)
        elif self.is_long_click():
            return self.radio_action.check_and_execute(ButtonClickStates.BUTTON_STATE_LONG_CLICK,
                                                       sensor_msg_updated,
                                                       sensor_msg_old)
        elif self.is_double_click():
            return self.radio_action.check_and_execute(ButtonClickStates.BUTTON_STATE_DOUBLE_CLICK,
                                                       sensor_msg_updated,
                                                       sensor_msg_old)

    # TODO: Test this with min max
    def get_frequency_stream(self, sensor_value: int) -> None | RadioFrequency:
        over_min_max_frequency = None
        for index, radio_frequency in enumerate(self.frequency_list.frequencies):
            try:
                if radio_frequency.minimum <= sensor_value < radio_frequency.maximum:
                    return radio_frequency
                elif index == 0 and sensor_value < radio_frequency.minimum:
                    over_min_max_frequency = radio_frequency
                elif index == len(self.frequency_list.frequencies) and sensor_value > radio_frequency.maximum:
                    over_min_max_frequency = radio_frequency
            except TypeError:
                return None
        return over_min_max_frequency

    def _is_click(self, threshold: int):
        # TODO: measure is click with time
        counter = 0
        for value in self.state.states:
            if value is True:
                counter += 1
                if counter > threshold:
                    return True
            else:
                return False
        return False

    def is_short_click(self):
        return self._is_click(self.short_threshold)

    def is_long_click(self):
        return self._is_click(self.long_threshold)

    def is_double_click(self):
        # TODO
        return False
        raise NotImplemented


class AnalogProcessData:
    def __init__(self, pin: int, name: str, is_frequency: bool, frequencies: Frequencies):
        self.name: str = name
        self.pin: int = pin
        self.is_frequency: bool = is_frequency
        self.frequency_list: Frequencies = frequencies
        self.data: AnalogData = AnalogData()