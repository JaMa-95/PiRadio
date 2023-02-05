from gpiozero import Button
from signal import pause
import time
import _thread

run = False


def do_stuff():
    while run:  # do stuff...
        time.sleep(1)
        print("waiting...")


def first_button():
    global run
    print("First Pressed")
    run = True
    _thread.start_new_thread(do_stuff)


def second_button():
    global run
    print("Second Pressed")
    run = False


b1 = Button(7)
b1.when_pressed = first_button
b2 = Button(8)
b2.when_pressed = second_button