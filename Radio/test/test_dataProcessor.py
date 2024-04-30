import unittest
from Radio.dataProcessor import DataProcessor
from Radio.sensorMsg import AnalogData, AnalogValue


class TestDataProcessor(unittest.TestCase):
    def test_init(self):
        data_processor = DataProcessor()

    def test_analog(self):
        data_processor = DataProcessor()
        analog_data = AnalogData()
        analog_data.set_data([AnalogValue(1, 0)])
        data_processor.process_analogs(analog_data)