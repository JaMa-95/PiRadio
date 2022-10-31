from subprocess import call


class Raspberry:
    @staticmethod
    def turn_raspi_off():
        print("turn off raspi")
        call("sudo shutdown -h now", shell=True)

    @staticmethod
    def turn_off_usb():
        call("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind")

    @staticmethod
    def turn_on_usb():
        call("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/bind")