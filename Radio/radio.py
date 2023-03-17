import datetime
import sys
import glob
import serial
import time
import traceback
from dataclasses import dataclass
import RPi.GPIO as GPIO

from radioFrequency import RadioFrequency, KurzFrequencies, LangFrequencies, MittelFrequencies, UKWFrequencies, \
    SprFrequencies
from button import RadioButtonsRaspi
from db.db import Database
from raspberry import Raspberry
from mqtt.mqttBroker import MqttBroker
from led.ledStrip import LedStrip, LedData


# TODO: Add web control
@dataclass
class Speakers:
    play_radio: bool = True
    play_central: bool = False

    _change_wait: bool = datetime.datetime.now()

    def change(self, play_central: bool, play_radio: bool):
        self.play_radio = play_radio
        self.play_central = play_central

    def change_once(self):
        now = datetime.datetime.now()
        change_delta = now - self._change_wait
        if change_delta.seconds > 2:
            self._change_wait = now
            if self.play_radio and self.play_central:
                print("CHANGE SPEAKER TO CENTRAL")
                self.play_radio = False
            elif self.play_radio:
                print("CHANGE SPEAKER TO CENTRAL/RADIO")
                self.play_central = True
            elif self.play_central:
                print("CHANGE SPEAKER TO RADIO")
                self.play_central = False
                self.play_radio = True


class Radio:
    def __init__(self, mqtt: bool, play_central: bool, play_radio_speaker: bool) -> None:
        # init pub
        self.__subscribers = []
        self.__content = None

        self.raspberry = Raspberry()
        self.playing = False
        self.on = False

        self.amplifier_switch_pin = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.amplifier_switch_pin, GPIO.OUT)

        self.speakers = Speakers(play_radio=play_radio_speaker, play_central=play_central)

        self.current_volume_poti_value = 0
        self.poti_values = [0, 0, 0]
        self.poti_value_index = 0

        self.pin_mittel = 3
        self.pin_volume = 2

        self.radio_buttons = RadioButtonsRaspi()

        self.current_stream: RadioFrequency = RadioFrequency("", 0, 0, "", "")
        self.current_command = {"buttonOnOff": None, "buttonLang": None, "buttonMittel": None, "buttonKurz": None,
                                "buttonUKW": None, "buttonSprMus": None, "potiValue": None, "posLangKurzMittel": None,
                                "posUKW": None}
        self.old_command = {"buttonOnOff": None, "buttonLang": None, "buttonMittel": None, "buttonKurz": None,
                            "buttonUKW": None, "buttonSprMus": None, "potiValue": None, "posLangKurzMittel": None,
                            "posUKW": None}
        self.currentCommandString = None
        self.volume_old = None
        self.volume_sensitivity = 1
        self.poti_sensivity = 3
        self.broker: MqttBroker = None
        self.mqtt = mqtt
        if mqtt:
            self.connect_mqtt()

        self.ledData = LedData.instance()
        self.ledStrip = LedStrip()
        self.db = Database()

    # PUB METHODS
    def attach(self, subscriber):
        self.__subscribers.append(subscriber)

    def detach(self):
        self.__subscribers.pop()

    def get_subscribers(self):
        return [type(x).__name__ for x in self.__subscribers]

    def update_subscribers(self):
        for sub in self.__subscribers:
            sub.update()

    def add_content(self, content):
        self.__content = content

    def get_content(self):
        return self.__content

    def publish(self, data):
        self.add_content(data)
        self.update_subscribers()

    # END PUB METHODS

    def connect_mqtt(self):
        self.broker = MqttBroker()
        self.broker.connect_mqtt()
        self.broker.client.loop_start()

    def run(self):
        self.ledData.fade = True
        self.ledData.one_after_another = True
        self.ledData.blink_twice = True
        self.ledData.all_on = True

        print("start checking commands")
        self.turn_off_amplifier()
        while True:
            self.check_radio_on_off()
            self.check_raspi_off()
            self.check_esp_reset()
            self.check_change_speakers()
            changed_hardware = self.get_changed_buttons()
            changed_hardware.extend(self.get_changed_hardware())
            if changed_hardware:
                self.process_hardware_change(changed_hardware)
            time.sleep(0.01)

    def check_raspi_off(self):
        if self.radio_buttons.button_on_off.long_click():
            self.raspberry.turn_raspi_off()

    def check_radio_on_off(self):
        if self.radio_buttons.button_on_off.is_click():
            self.on = not self.on
            if self.on:
                self.turn_on_radio()
            else:
                self.turn_off_radio()

    def check_change_speakers(self):
        if self.radio_buttons.button_on_off.double_click():
            self.speakers.change_once()
            if not self.speakers.play_radio:
                self.publish("stop")
            if self.mqtt:
                if not self.speakers.play_central:
                    self.broker.publish_start_stop("0")

    def check_esp_reset(self):
        if self.radio_buttons.button_spr.long_click():
            print("RESET ESP")
            self.raspberry.turn_off_usb()
            time.sleep(2)
            self.raspberry.turn_on_usb()

    def set_old_command(self, command_):
        self.old_command["buttonOnOff"] = command_["buttonOnOff"]
        self.old_command["buttonLang"] = command_["buttonLang"]
        self.old_command["buttonMittel"] = command_["buttonMittel"]
        self.old_command["buttonKurz"] = command_["buttonKurz"]
        self.old_command["buttonUKW"] = command_["buttonUKW"]
        self.old_command["buttonSprMus"] = command_["buttonSprMus"]
        self.old_command["potiValue"] = command_["potiValue"]
        self.old_command["posLangKurzMittel"] = command_["posLangKurzMittel"]
        self.old_command["posUKW"] = command_["posUKW"]

    def process_hardware_change(self, changed_hardware_list):
        for changed_hardware in changed_hardware_list:
            if changed_hardware == "potiValue":
                self.set_volume(self.current_command[changed_hardware])
            else:
                if changed_hardware in ["posLangKurzMittel", "posUKW"]:
                    pass
                    # print("------------------------------------")
                    # print(f"encoder changed {self.current_command['posLangKurzMittel']}, "
                    #       f"{self.current_command['posUKW']}")
                self.process_hardware_value_change()

    def turn_off_amplifier(self):
        print("TURN OFF")
        GPIO.output(4, False)

    def turn_on_amplifier(self):
        print("Turn ON")
        GPIO.output(4, True)

    def turn_on_radio(self):
        print("Turning on Radio")
        radio_frequency, encoder_value = self.get_button_frequency()
        if radio_frequency and self.on:
            stream = self.get_frequency_stream(radio_frequency, encoder_value)
            print("stream: ", stream)
            if stream:
                if self.current_stream.radio_url != stream.radio_url:
                    self.start_stream(stream)
        else:
            print("No button pressed. Playing nothing")

    def turn_off_radio(self):
        print("Turning off radio")
        if self.speakers.play_radio:
            self.publish("stop")
        self.turn_off_amplifier()
        self.current_stream.radio_url = None
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_start_stop("0")

    def start_stream(self, stream: RadioFrequency):
        print(f"Playing stream: {stream}")
        self.turn_on_amplifier()
        if self.speakers.play_radio:
            self.publish(stream)
        self.db.replace_stream(stream.radio_url)
        self.db.replace_radio_name(stream.name + "; " + stream.radio_name)
        self.current_stream = stream
        self.playing = True
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_start_stop("1")
                self.broker.publish_stream(stream.radio_url)

    @staticmethod
    def get_frequency_stream(button_frequencies, encoder_value):
        for radio_frequency in button_frequencies.frequencies:
            if radio_frequency.minimum <= encoder_value < radio_frequency.maximum:
                return radio_frequency
        return None

    def get_button_frequency(self):
        if self.radio_buttons.button_lang.state:
            return LangFrequencies(), self.current_command["posLangKurzMittel"]
        elif self.radio_buttons.button_mittel.state:
            return MittelFrequencies(), self.current_command["posLangKurzMittel"]
        elif self.radio_buttons.button_kurz.state:
            return KurzFrequencies(), self.current_command["posLangKurzMittel"]
        elif self.radio_buttons.button_ukw.state:
            return UKWFrequencies(), self.current_command["posUKW"]
        elif self.radio_buttons.button_spr.state:
            return SprFrequencies(), self.current_command["posUKW"]
        else:
            # print("using NONE")
            return None, None

    def set_volume(self, volume):
        volume = int(0.00606 * volume - 63.63)
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        print(f"volume: {volume}")
        self.db.replace_volume(volume)
        self.send_volume(volume)

    def set_poti_value(self, poti):
        self.poti_values[self.poti_value_index] = poti

        self.poti_value_index = (self.poti_value_index + 1) % len(self.poti_values)

    def get_poti_value(self):
        value = 0
        for poti_value in self.poti_values:
            value += poti_value
        value = value / len(self.poti_values)
        return value

    def difference_poti_high(self, poti):
        self.set_poti_value(poti)
        poti = self.get_poti_value()
        if poti > self.current_volume_poti_value:
            if poti > (self.current_volume_poti_value + self.poti_sensivity):
                self.current_volume_poti_value = poti
                return True
        elif poti < (self.current_volume_poti_value - self.poti_sensivity):
            self.current_volume_poti_value = poti
            return True
        return False

    def send_volume(self, volume):
        self.volume_old = volume
        if self.speakers.play_radio:
            self.publish(volume)
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_volume(volume)

    def extract_commands_from_string(self, command_: str):
        command_name = ""
        command_value = ""
        process_name = True
        for char in command_:
            if char == ":":
                process_name = False
            elif char == ";":
                try:
                    self.current_command[command_name] = int(command_value)
                    return 0
                except ValueError as e:
                    print(print(traceback.format_exc()))
                    print(command_value)
            elif char == ",":
                process_name = True
                try:
                    self.current_command[command_name] = int(command_value)
                except ValueError as e:
                    print(print(traceback.format_exc()))
                    print(command_value)
                command_name = ""
                command_value = ""
            elif process_name:
                command_name += char
            else:
                command_value += char

    """
    returns what hardware changed
    for example sound volume, frequency, ...
    """
    def get_changed_hardware(self):
        changed_hardware = []
        value = self.db.get_ads_pin_value(self.pin_mittel)
        if value != self.old_command["posLangKurzMittel"]:
            changed_hardware.append("posLangKurzMittel")
            self.current_command["posLangKurzMittel"] = value
        value = self.db.get_ads_pin_value(self.pin_volume)
        if self.difference_poti_high(value):
            changed_hardware.append("potiValue")
            self.current_command["potiValue"] = value
        return changed_hardware

    def get_changed_buttons(self):
        self.radio_buttons.set_value()
        changed_hardware = []
        state = self.radio_buttons.button_on_off.state
        if self.current_command["buttonOnOff"] != state:
            print(f"BUTTON ON OFF CHANGED {state}")
            self.current_command["buttonOnOff"] = state
            changed_hardware.append("buttonOnOff")
        state = self.radio_buttons.button_lang.state
        if self.current_command["buttonLang"] != state:
            print(f"BUTTON LANG CHANGED: {state}")
            self.current_command["buttonLang"] = state
            changed_hardware.append("buttonLang")
        state = self.radio_buttons.button_mittel.state
        if self.current_command["buttonMittel"] != state:
            print(f"BUTTON MITTEL CHANGED: {state}")
            self.current_command["buttonMittel"] = state
            changed_hardware.append("buttonMittel")
        state = self.radio_buttons.button_kurz.state
        if self.current_command["buttonKurz"] != state:
            print(f"BUTTON KURZ CHANGED: {state}")
            self.current_command["buttonKurz"] = state
            changed_hardware.append("buttonKurz")
        state = self.radio_buttons.button_ukw.state
        if self.current_command["buttonUKW"] != state:
            print(f"BUTTON UKW CHANGED: {state}")
            self.current_command["buttonUKW"] = state
            changed_hardware.append("buttonUKW")
        state = self.radio_buttons.button_spr.state
        if self.current_command["buttonSprMus"] != state:
            print(f"BUTTON SPR CHANGED: {state}")
            self.current_command["buttonSprMus"] = state
            changed_hardware.append("buttonSprMus")
        return changed_hardware

    def process_hardware_value_change(self):
        radio_frequency, encoder_value = self.get_button_frequency()
        if radio_frequency and self.on:
            stream = self.get_frequency_stream(radio_frequency, encoder_value)
            if stream:
                if self.current_stream.radio_url != stream.radio_url:
                    print("Changing stream")
                    if self.playing:
                        if self.speakers.play_radio:
                            self.publish("stop")
                        self.playing = False
                    if radio_frequency:
                        print(f"Playing playlist: {stream}")
                        self.db.replace_stream(stream.radio_url)
                        self.db.replace_radio_name(stream.name + "; " + stream.radio_name)
                        self.turn_on_amplifier()
                        if self.speakers.play_radio:
                            self.publish(stream)
                        self.playing = True
                        self.current_stream = stream
                        if self.mqtt:
                            if self.speakers.play_central:
                                self.broker.publish_start_stop("1")
                                self.broker.publish_stream(stream.radio_url)

    def stop_player(self):
        if self.speakers.play_radio:
            self.publish("stop")
        # global_.stop = True
        self.current_stream.radio_url = None
        if self.mqtt:
            if self.speakers.play_central:
                self.broker.publish_start_stop("0")

    def error(self):
        # save error cause
        # light up red lamp
        pass


class USBReader:
    @staticmethod
    def serial_ports():
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def get_usb_ser_linux(self):
        serial_ports = self.serial_ports()
        print(serial_ports)
        run = True
        counter = 0
        while run:
            if counter == 5:
                try:
                    ser = serial.Serial(port="dev/ttyUSB1", baudrate=500000)
                    return ser
                except serial.serialutil.SerialException:
                    print("Try USB1 failed")
                    counter = 0
            for device in serial_ports:
                if "USB" in device:
                    try:
                        ser = serial.Serial(port=device, baudrate=500000)
                    except serial.serialutil.SerialException:
                        print("Unplugged device")
                    print(f"Using: {device}")
                    # success = self.check_connection(ser)
                    # if not success:
                    # sys.stdout.flush()
                    return ser
                    print("Connection failed")
            serial_ports = self.serial_ports()
            print(serial_ports)
            print("ESP not connected. Waiting ...")
            # sys.stdout.flush()
            counter += 1
            time.sleep(1)

    def get_usb_ser_linux_2(self):
        serial_ports = self.serial_ports()
        print(serial_ports)
        run = True
        counter = 0
        while run:
            for device in serial_ports:
                if "USB" in device:
                    try:
                        ser = serial.Serial(port=device, baudrate=500000)
                    except serial.serialutil.SerialException:
                        print("Unplugged device")
                    print(f"Using: {device}")
                    return ser
            serial_ports = self.serial_ports()
            print(serial_ports)
            print("ESP not connected. Waiting ...")
            # sys.stdout.flush()
            counter += 1
            time.sleep(1)

    def get_usb_ser_win(self):
        serial_ports = self.serial_ports()
        while len(serial_ports) == 0:
            serial_ports = self.serial_ports()
            print("ESP not connected. Waiting ...")
            # sys.stdout.flush()
            time.sleep(1)
        print(f"Using: {serial_ports[0]}")
        # sys.stdout.flush()
        ser = serial.Serial(port=serial_ports[0], baudrate=500000)
        return ser

    def get_usb_ser(self):
        if sys.platform.startswith('linux'):
            ser = self.get_usb_ser_linux_2()
        else:
            ser = self.get_usb_ser_win()
        return ser

    @staticmethod
    def check_connection(ser):
        try:
            if ser.read():
                return True
        except serial.serialutil.SerialException:
            return False

    def read_usb(self):
        # compare with old usb string
        # update new values
        # update usb string
        ser = self.get_usb_ser()
        print("Start running")
        global command
        while True:
            if ser.in_waiting > 1000:
                ser.flushInput()
            try:
                command_ = ser.read_until(b';').decode("UTF-8")
                command_ = command_.replace("\n", "").replace("\r", "")
                if command_[0] == "-" and command_[-1] == ";":
                    command = command_[1:]
            except UnicodeDecodeError or serial.serialutil.SerialException as e:
                print(print(traceback.format_exc()))
                if e == serial.serialutil.SerialException and "readiness" in e:
                    pass  # error 2

    def set_test_command(self, command_):
        global command
        command = command_
