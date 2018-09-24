Overall this is extending the etch-a-sketch to run off encoders and LED matrix. 
This homework also uses i2c to control the LED matrix and two temp sensors.

# PROGRAMS
* encoder.py - This is the led matrix using the encoders.
* main.py - This program uses the keys and buttons to control the led matrix
* setup.sh - sets up the pins for the encoder
* tmp101reading.sh - prints out the two temp sensors one time to the screen

# RUN
## encoder.py
If you haven't set the pins for the encoder make sure you run `./setup.sh` to configure the pins.

To start run `$bone ./encoder.py`

This program takes the input from two encoders to control the led matrix.
The program doesn't ask for board size it is already set to the size of the matrix.

To control you need to wire up the encoders and buttons like so:
```
CLEAR_BUTTON =  "P9_42"
EXIT_BUTTON = "P9_27"

ENCODER 1:
A = "P8_35"
B = "P8_33"

ENCODER 2:
A = "P8_42"
B = "P8_41"

LED matrix needs to be wired to i2c
```

Encoder 1 is left and right.

Encoder 2 is up and down.

The buttons clear and exit the game board.

## main.py
This is the overall Etch-e-sketch program. This is setup to run on off of buttons.
You set the size of the board from the screen and if you reach the end of the LED matrix it will stop
but continue on screen. It runs both the LED matrix and screen for this program.

It will also work with the default keyboard buttons:
```
'w' - up
's' - down
'a' - left
'd' - right
'e' - exit
'c' - clear
```

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

## tmp101reading.sh
This program reads the two temp sensors on the i2c bus. One the add0 pin is left floating
and the other is tied to ground. 

run by typing `$bone ./tmp101reading.sh`

All of this has been tested and verified. 

========================
Professor Yoder's Comments

Looks very good again.  Nice and complete.

Score:10/10