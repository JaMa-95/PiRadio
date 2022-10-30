import sys
import glob
import serial
import time
import traceback
from radioFrequency import RadioFrequency, KurzFrequencies, LangFrequencies, MittelFrequencies, UKWFrequencies, \
    SprFrequencies
from db.db import Database
from raspberry import Raspberry
from mqtt.mqttBroker import MqttBroker

command = None
glAudioPlayer = None
stop = False


class Radio:
    def __init__(self, mqtt: bool, play_central: bool, play_speaker: bool) -> None:
        # init pub
        self.__subscribers = []
        self.__content = None

        self.play_central = play_central
        self.play_speaker = play_speaker

        # init radio frequencies
        self.raspberry = Raspberry()
        self.playing = False
        self.audio_player_thread = None
        self.button_threshold = 30
        self.on = False
        self.on_off_wait = False
        self.on_off_counter = 0
        self.spr_counter = 0
        self.current_stream: RadioFrequency = RadioFrequency("", 0, 0, "", "")
        self.current_command = {"buttonOnOff": None, "buttonLang": None, "buttonMittel": None, "buttonKurz": None,
                                "buttonUKW": None, "buttonSprMus": None, "potiValue": None, "posLangKurzMittel": None,
                                "posUKW": None}
        self.old_command = {"buttonOnOff": None, "buttonLang": None, "buttonMittel": None, "buttonKurz": None,
                            "buttonUKW": None, "buttonSprMus": None, "potiValue": None, "posLangKurzMittel": None,
                            "posUKW": None}
        self.currentCommandString = None
        self.volume_old = None
        self.volume_sensitivity = 2

        self.broker: MqttBroker = None
        self.mqtt = mqtt
        self.connect_mqtt()

        self.db = Database()


    # PUB METHODS
    def attach(self, subscriber):
        self.__subscribers.append(subscriber)

    def detach(self):
        self.__subscribers.pop()

    def get_subscribers(self):
        return [type(x).__name__ for x in self.__subscribers]

    def updateSubscribers(self):
        for sub in self.__subscribers:
            sub.update()

    def add_content(self, content):
        self.__content = content

    def get_content(self):
        return self.__content

    def publish(self, data):
        self.add_content(data)
        self.updateSubscribers()

    # END PUB METHODS

    def connect_mqtt(self):
        self.broker = MqttBroker()
        self.broker.connect_mqtt()
        self.broker.client.loop_start()

    def check_commands(self):
        global command
        counter = 0
        while True:
            if counter % 10 == 0:
                pass  # print(self.current_command["posLangKurzMittel"], self.current_command["posUKW"])
            counter += 1
            if self.current_command["buttonOnOff"]:
                self.button_counter("buttonOnOff")
            if self.current_command["buttonSprMus"]:
                self.button_counter("buttonSprMus")
            self.check_raspi_off()
            if command != self.currentCommandString:
                self.set_old_command(self.current_command)
                self.currentCommandString = command
                self.extract_commands_from_string(command)
                changed_hardware = self.get_changed_hardware()
                if changed_hardware:
                    self.process_hardware_change(changed_hardware)
            time.sleep(0.01)

    def reset_all(self):
        # TODO: reset poti, position
        pass

    def check_raspi_off(self):
        if self.on_off_counter > 400 and self.spr_counter > 400:
            self.raspberry.turn_raspi_off()

    def button_counter(self, button_name):
        if self.current_command[button_name] > 30:
            if button_name == "buttonOnOff":
                self.on_off_counter = 0
                self.on_off_wait = False
            else:
                self.spr_counter = 0
        else:
            if button_name == "buttonOnOff":
                self.on_off_counter += 1
                if self.on_off_counter > 10 and not self.on_off_wait:
                    self.turn_on_off_radio(self.current_command[button_name])
                    self.on_off_wait = True
            else:
                self.spr_counter += 1

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
                # print("volume changed")
                self.set_volume(self.current_command[changed_hardware])
            elif changed_hardware in ["buttonLang", "buttonMittel", "buttonKurz", "buttonUKW", "buttonSprMus"]:
                print("button changed")
                print("------------------------------------")
                self.process_hardware_value_change()
            elif changed_hardware in ["posLangKurzMittel", "posUKW"]:
                print("------------------------------------")
                print("encoder changed")
                self.process_hardware_value_change()

    def turn_on_off_radio(self, value):
        # TODO: turn on/off music
        # TODO: turn on/off lights?
        # TODO: when turn on check everything and play
        if value < 30:
            if self.on_off_counter > 5:
                self.on = not self.on
                if self.on:
                    self.turn_on_radio()
                else:
                    self.turn_off_radio()

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
        if self.play_speaker:
            self.publish("stop")
        # global_.stop = True
        self.current_stream.radio_url = None
        if self.mqtt:
            if self.play_central:
                self.broker.publish_start_stop("0")

    def start_stream(self, stream: RadioFrequency):
        print(f"Playing stream: {stream}")
        if self.play_speaker:
            self.publish(stream)
        self.current_stream = stream
        self.playing = True
        if self.mqtt:
            if self.play_central:
                self.broker.publish_start_stop("1")
                self.broker.publish_stream(stream.radio_url)

    @staticmethod
    def get_frequency_stream(button_frequencies, encoder_value):
        for radio_frequency in button_frequencies.frequencies:
            if radio_frequency.minimum <= encoder_value < radio_frequency.maximum:
                return radio_frequency

    def get_button_frequency(self):
        pressed_button = self.get_pressed_button()
        if pressed_button == "buttonLang":
            return LangFrequencies(), self.current_command["posLangKurzMittel"]
        elif pressed_button == "buttonMittel":
            return MittelFrequencies(), self.current_command["posLangKurzMittel"]
        elif pressed_button == "buttonKurz":
            return KurzFrequencies(), self.current_command["posLangKurzMittel"]
        elif pressed_button == "buttonUKW":
            return UKWFrequencies(), self.current_command["posUKW"]
        elif pressed_button == "buttonSprMus":
            return SprFrequencies(), self.current_command["posUKW"]
        else:
            return None, None

    def get_pressed_button(self):
        for button, value in self.current_command.items():
            if value < self.button_threshold and button != "buttonOnOff":
                return button
            elif button == "posLangKurzMittel":
                # reached end of buttons
                return None

    def set_volume(self, volume):
        volume = int((volume - 1500) / 25.95)
        # volume raspberry
        volume = int(volume / 1.5)
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100

        self.db.insert_volume(volume)
        if self.volume_old:
            if self.difference_volume_high(volume):
                self.send_volume(volume)
        else:
            self.send_volume(volume)

    def difference_volume_high(self, volume):
        if volume > self.volume_old:
            if volume > (self.volume_old + self.volume_sensitivity):
                return True
        elif volume < (self.volume_old - self.volume_sensitivity):
            return True
        return False

    def send_volume(self, volume):
        self.volume_old = volume
        if self.play_speaker:
            self.publish(volume)
        if self.mqtt:
            if self.play_central:
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
        for command_, value in self.current_command.items():
            if value and self.old_command[command_]:
                if command_ == "posLangKurzMittel" or command_ == "posUKW" or command_ == "potiValue":
                    if value != self.old_command[command_]:
                        changed_hardware.append(command_)
                if (value / self.old_command[command_]) < 0.5 and value < self.button_threshold \
                        and self.old_command[command_] > 30:
                    changed_hardware.append(command_)
                elif value > 30 and self.old_command[command_] < 30:
                    changed_hardware.append(command_)
        self.update_db(changed_hardware)
        return changed_hardware

    def update_db(self, changed_hardware):
        if "posLangKurzMittel" in changed_hardware:
            self.db.insert_pos_lang_mittel_kurz(self.current_command["posLangKurzMittel"])
        if "posUKW" in changed_hardware:
            self.db.insert_pos_ukw(self.current_command["posUKW"])
        if "buttonOnOff" in changed_hardware:
            self.db.insert_button_on_off(self.current_command["buttonOnOff"])
        if "buttonLang" in changed_hardware:
            self.db.insert_button_lang(self.current_command["buttonOnOff"])
        if "buttonMittel" in changed_hardware:
            self.db.insert_butto_mittel(self.current_command["buttonOnOff"])
        if "buttonKurz" in changed_hardware:
            self.db.insert_button_kurz(self.current_command["buttonOnOff"])
        if "buttonUKW" in changed_hardware:
            self.db.insert_button_ukw(self.current_command["buttonOnOff"])
        if "buttonSprMus" in changed_hardware:
            self.db.insert_button_spr_mus(self.current_command["buttonOnOff"])

    def process_hardware_value_change(self):
        radio_frequency, encoder_value = self.get_button_frequency()
        if radio_frequency and self.on:
            stream = self.get_frequency_stream(radio_frequency, encoder_value)
            if stream:
                if self.current_stream.radio_url != stream.radio_url:
                    print("Changing stream")
                    if self.playing:
                        if self.play_speaker:
                            self.publish("stop")
                        self.playing = False
                        # self.stop_player()
                        print("STOP")
                        time.sleep(1)
                        # self.audio_player_thread = None
                        # print(self.audio_player_thread)
                    if radio_frequency:
                        print(f"Playing playlist: {stream}")
                        if self.play_speaker:
                            self.publish(stream)

                        self.playing = True
                        # self.audio_player_thread = AudioPlayer(stream, encoder_value)
                        # global_.stop = False
                        # self.audio_player_thread.start()
                        self.current_stream = stream
                        if self.mqtt:
                            if self.play_central:
                                self.broker.publish_start_stop("1")
                                self.broker.publish_stream(stream.radio_url)
        #elif self.audio_player_thread and button:
        #    self.stop_player()

    def stop_player(self):
        if self.play_speaker:
            self.publish("stop")
        # global_.stop = True
        self.current_stream.radio_url = None
        if self.mqtt:
            if self.play_central:
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
