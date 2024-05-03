import unittest

from Radio.RadioAction import Actions, HoldFrequencyX, ButtonClickStates, PlayMusic
from Radio.dataProcessor import DataProcessor
from Radio.sensorMsg import AnalogData, AnalogValue


class TestDataProcessor(unittest.TestCase):
    def test_init(self):
        data_processor = DataProcessor()

    def test_analog_init(self):
        data_processor = DataProcessor()
        self.assertEqual(data_processor.analog_processor.analog_items[0].name, "posLangKurzMittel")
        self.assertEqual(len(data_processor.analog_processor.analog_items), 4)

    def test_button_init(self):
        data_processor = DataProcessor()
        self.assertEqual(data_processor.button_processor.buttons[0].name, "OnOffRaspi")
        self.assertEqual(len(data_processor.button_processor.buttons), 9)

class TestAnalogProcessor(unittest.TestCase):
    def test_analog_frequency(self):
        data_processor = DataProcessor()
        analog_data = AnalogData()
        pin = 3
        for data in analog_data.get_data_sensor():
            if data.pin == pin:
                self.assertEqual(data.value, 0)
        analog_data.set_data([AnalogValue(pin, 101)])
        for data in analog_data.get_data_sensor():
            if data.pin == pin:
                self.assertEqual(data.value, 101)

        actions = Actions()
        actions.add_action(HoldFrequencyX(pin, ButtonClickStates.BUTTON_STATE_ON))
        data_processor.process_analogs(analog_data,
                                       actions)

        for item in data_processor.analog_processor.analog_items:
            if item.pin == pin:
                self.assertEqual(item.value, 101)

    def test_analog_frequency_stream(self):
        data_processor = DataProcessor()
        analog_data = AnalogData()
        pin = 3
        for data in analog_data.get_data_sensor():
            if data.pin == pin:
                self.assertEqual(data.value, 0)
        analog_data.set_data([AnalogValue(pin, 101)])
        for data in analog_data.get_data_sensor():
            if data.pin == pin:
                self.assertEqual(data.value, 101)

        actions = Actions()
        actions.add_action(PlayMusic(pin, "Ta", "posLangKurzMittel"))
        data_processor.process_analogs(analog_data,
                                       actions)

        for item in data_processor.analog_processor.analog_items:
            if item.pin == pin:
                self.assertEqual(item.value, 101)

    def test_analog_volume(self):
        data_processor = DataProcessor()
        analog_data = AnalogData()
        pin = 1
        value = 30000
        mapped_value = 100  # 30000 maps to value 100
        for data in analog_data.get_data_sensor():
            if data.pin == pin:
                self.assertEqual(data.value, 0)
        analog_data.set_data([AnalogValue(pin, value)])
        for data in analog_data.get_data_sensor():
            if data.pin == pin:
                self.assertEqual(data.value, value)

        actions = Actions()
        actions.add_action(HoldFrequencyX(pin, ButtonClickStates.BUTTON_STATE_ON))
        data_processor.process_analogs(analog_data,
                                       actions)

        for item in data_processor.analog_processor.analog_items:
            if item.pin == pin:
                self.assertEqual(item.value, mapped_value)

    def test_analog_bass(self):
        data_processor = DataProcessor()
        analog_data = AnalogData()
        pin = 2
        value = 30000
        mapped_value = 20  # 30000 maps to value 20
        for data in analog_data.get_data_sensor():
            if data.pin == pin:
                self.assertEqual(data.value, 0)
        analog_data.set_data([AnalogValue(pin, value)])
        for data in analog_data.get_data_sensor():
            if data.pin == pin:
                self.assertEqual(data.value, value)

        actions = Actions()
        actions.add_action(HoldFrequencyX(pin, ButtonClickStates.BUTTON_STATE_ON))
        data_processor.process_analogs(analog_data,
                                       actions)

        for item in data_processor.analog_processor.analog_items:
            if item.pin == pin:
                self.assertEqual(item.value, mapped_value)
