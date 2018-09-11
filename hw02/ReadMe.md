# PROGRAMS
* blinkLED.c - this program toggles the led on GPIO 60 at the compiled rate
* ledToggle.py - this program is the python version of LED toggle. 
                    If you want different rates you have to change "delay".
* install.sh - installs the libsoc for gpio toggle in c
* Makefile - compiles blinkLED.c into an execute able.
* toggleComparison.docx - document that describes the results of led toggling.
* buttonToggleLED.py - Toggles 4 LEDS if one of the 4 buttons are pressed. Each
                        LED lights up based on one of the buttons.

# RUN
## blinkLED
* If you don't have the libsoc libraries install run `./install.sh` before compiling.

To run this hook up an led to GPIO 60. Run `make` to compile the program.

To use run `./blinkLED <delay(us)>` to use the program.

## ledToggle.py
To use this hook up an led to GPIO 60. Run `./ledToggle.py`. To change the delay
fix the delay variable in the file.

## main.py
This is the overall Etch-e-sketch program. This is setup to run on off of buttons.

The defualt buttons are wired like this:
```
LEFT_BUTTON =  "P9_42"
RIGHT_BUTTON = "P9_27"
UP_BUTTON = "P9_25"
DOWN_BUTTON = "P9_23"
```
The buttons should be hooked up like this. Run `./main.py` to run the program.

You can control the directions with the buttons. To exit press `e` and to clear
press `c`.

## buttonToggleLED.py
This programs runs four buttons and turns on 4 LEDS based on the button press.

You need to connect the LEDs and Buttons like this:
```
LED1 = "P8_45"
LED2 = "P8_46"
LED3 = "P8_44"
LED4 = "P8_43"

BUTTON1 = "P9_42"
BUTTON2 = "P9_27"
BUTTON3 = "P9_25"
BUTTON4 = "P9_23"
```

run the program `./buttonToggleLED.py`
