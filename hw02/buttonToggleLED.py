#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time

LED1 = "P8_45"
LED2 = "P8_46"
LED3 = "P8_44"
LED4 = "P8_43"

BUTTON1 = "P9_42"
BUTTON2 = "P9_27"
BUTTON3 = "P9_25"
BUTTON4 = "P9_23"

# Set the GPIO pins:
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

GPIO.setup(BUTTON1, GPIO.IN)
GPIO.setup(BUTTON2, GPIO.IN)
GPIO.setup(BUTTON3, GPIO.IN)
GPIO.setup(BUTTON4, GPIO.IN)

# map of buttons to leds
map = {BUTTON1 : LED1, BUTTON2 : LED2, BUTTON3 : LED3, BUTTON4 : LED4}

def updateLED(channel):
    print("Button pressed")
    state = GPIO.input(channel)
    GPIO.output(map[channel], state)
    
# attach events to listen to buttons
GPIO.add_event_detect(BUTTON1, GPIO.BOTH, callback=updateLED, bouncetime=100)
GPIO.add_event_detect(BUTTON2, GPIO.BOTH, callback=updateLED, bouncetime=100)
GPIO.add_event_detect(BUTTON3, GPIO.BOTH, callback=updateLED, bouncetime=100)
GPIO.add_event_detect(BUTTON4, GPIO.BOTH, callback=updateLED, bouncetime=100)

try:
    while True:
        time.sleep(100) # don't hog CPU
        
except KeyboardInterrupt:
    print("Cleaning up")
    GPIO.cleanup()
    
GPIO.cleanup()