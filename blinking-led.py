#Resource: https://raspberrypihq.com/making-a-led-blink-using-the-raspberry-pi-and-python/
#Title: Simple Blinking LED code
#Capstone team: V2V project (Cameron, Austin & Aashima)

import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
class BlinkyLight:
    pin = 0
    freq = 1
    def __init__(self, pin, warnings = false, mode = GPIO.Board ):
        self.pin = pin

        GPIO.setwarnings(warnings)    # Ignore warning for now
        GPIO.setmode(mode)   # Use physical pin numbering
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)


    def run(self, freq):
        GPIO.output(self.pin, GPIO.HIGH) # Turn on
        sleep(1/freq)                  # Sleep for 2 second
        GPIO.output(self.pin, GPIO.LOW)  # Turn off
        sleep(1/freq)                  # Sleep for 1 second

