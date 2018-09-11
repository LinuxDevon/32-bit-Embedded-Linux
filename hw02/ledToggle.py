#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time

LED = "P9_12"
delay = 0.0001 # delay in seconds

# Set the GPIO pins:
GPIO.setup(LED, GPIO.OUT)

while True:
    GPIO.output(LED, 1)
    time.sleep(delay/2)
    GPIO.output(LED, 0)
    time.sleep(delay/2)