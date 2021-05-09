#Resource: https://raspberrypihq.com/making-a-led-blink-using-the-raspberry-pi-and-python/
#Title: Simple Blinking LED code
#Capstone team: V2V project (Cameron, Austin & Aashima)
import sys
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module
class BlinkyLight:
    pin = 0
    freq = 1
    def __init__(self, pin, warnings = False, mode = GPIO.BCM ):
        self.pin = pin

        GPIO.setwarnings(warnings)    # Ignore warning for now
        GPIO.setmode(mode)   # Use physical pin numbering
        GPIO.setup(pin, GPIO.OUT)   # Set pin 8 to be an output pin and set initial value to low (off)


    def run(self, freq):
        GPIO.output(self.pin, True) # Turn on
        sleep(1.0/freq)                  # Sleep for 1/f seconds
        GPIO.output(self.pin, False)  # Turn off
        sleep(1.0/freq)                  # Sleep for 1/f seconds

