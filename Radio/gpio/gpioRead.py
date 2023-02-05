import signal
import sys
import RPi.GPIO as GPIO

BUT_ON = 16
BUT_LANG = 18
BUT_MITTEL = 22
BUT_KURZ = 24
BUT_UKW = 26
BUT_SPR = 32

buttons = {"BUT_ON": 16}


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def button_pressed_callback(channel):
    print("-------------")
    print(f"Button pressed! {channel}")
    print("-------------")


if __name__ == '__main__':
    for button_name, button_io in buttons.items():
        print(button_name)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_io, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(button_io, GPIO.FALLING,
                              callback=button_pressed_callback, bouncetime=100)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()