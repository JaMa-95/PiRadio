from subprocess import call


class Raspberry:
    @staticmethod
    def turn_raspi_off():
        print("turn off raspi")
        call("sudo shutdown -h now", shell=True)
        # call(['shutdown', '-h', 'now'], shell=False)
