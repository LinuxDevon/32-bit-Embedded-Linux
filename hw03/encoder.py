#!/usr/bin/env python3
import curses
import smbus
import time
from curses import wrapper
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP2, eQEP1

# -- GLOBALS -- #
CLEAR_BUTTON =  "P9_42"
EXIT_BUTTON = "P9_27"
# UP_BUTTON = "P9_25"
# DOWN_BUTTON = "P9_23"

min_x = 3; min_y = 1;
max_x = 50; max_y = 50; # these are arbitrary for now incase of button clicks

# start cursor at top right corner
cursorPosX = min_x; cursorPosY = min_y;
gameArrayPosX = 14; gameArrayPosY = 0;
game_array = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01 ]
game = None
HEIGHT = 0; WIDTH = 0;

# -- MATRIX -- #
bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70

# -- ENCODERS -- #
Encoder1 = RotaryEncoder(eQEP1)
Encoder2 = RotaryEncoder(eQEP2)

running = True

# Starts the default settings for ncurses
# stdscr - the terminal window
def initCurses(stdscr):
    # Allow keystroke reading
    curses.noecho()

    # turn off buffered input
    curses.cbreak()

    # Enable arrow keys
    stdscr.keypad(True)

# Exits ncurses and does clean up
# stdscr - the terminal window
def exitCurses(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

# Create the start menu to guide the user. Also picks the window size
def makeMenu():
    begin_x = 0; begin_y = 0;
    height = curses.LINES; width = curses.COLS;

    # create the menu window
    menu = curses.newwin(height, width, begin_y, begin_x)
    
    # add the letters to the window
    menu.addstr(0, int(width / 2), "Etch A Sketch",curses.A_BLINK)
    menu.addstr(2, 0, "INSTRUCTIONS:")
    menu.addstr(3, 0, "Use encoders to control the led matrix with the encoder.")
    menu.addstr(5, 0, "button 1 to clear, button 2 to exit")
    menu.addstr(7, int(width / 4), "press any key to continue...");
    
    # update the window
    menu.refresh()

    # wait for user input
    menu.getch()

    width = 8
    length = 8
    
    # Delete the menu window
    menu.erase()
    menu.refresh()
    del menu
    return int(length), int(width) 

# Reads the input of the buttons and either exits or clears
# channel - the button pressed
def readButton(channel):
    global running, HEIGHT, WIDTH, game, game_array, gameArrayPosX, gameArrayPosY
    # clear
    if channel == CLEAR_BUTTON:
        createBoarder(game, HEIGHT, WIDTH)
        game_array = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ]
        game_array[gameArrayPosX+1] = game_array[gameArrayPosX+1] | (1 << gameArrayPosY) # add in the cursor
        bus.write_i2c_block_data(matrix, 0, game_array)
        
    # close
    if channel == EXIT_BUTTON:
        running = False

# Make the game window and run the game code
# height - the # of rows
# width - the # of columns
# stdscr - the terminal window
def createGameWindow(height, width, stdscr):
    global min_y, min_x, cursorPosX, cursorPosY, game, max_y, max_x
    global gameArrayPosX, gameArrayPosY, game_array, Encoder1, Encoder2, running
    global HEIGHT, WIDTH
    
    HEIGHT = height
    WIDTH  = width
    
    begin_x = 0; begin_y = 0;
    
    # bounds of the game board
    max_y = height+2; max_x = (2*width)+3;

    # create the gamec window
    game = curses.newwin(max_y, max_x, begin_y, begin_x)

    createBoarder(game, height, width)

    # move default cursor position
    game.move(cursorPosY, cursorPosX)
    
    GPIO.add_event_detect(CLEAR_BUTTON, GPIO.RISING, callback=readButton, bouncetime = 250)
    GPIO.add_event_detect(EXIT_BUTTON, GPIO.RISING, callback=readButton, bouncetime = 250)

    # verify that keys don't get echoed
    curses.noecho()
    
    # -- GAME LOOP -- #
    while running:
        game.addstr(cursorPosY, cursorPosX, "X")
        

        game_array[gameArrayPosX] = game_array[gameArrayPosX] | (1 << gameArrayPosY) # put x
        bus.write_i2c_block_data(matrix, 0, game_array)

            
        # Down
        if Encoder2.position < 0:
            Encoder2.position = 0
            if cursorPosY != (max_y - 2):
                game_array[gameArrayPosX+1] = 0x00 # remove cursor
                cursorPosY += 1
                gameArrayPosY += 1

        # Up
        elif Encoder2.position > 0:
            Encoder2.position = 0
            if cursorPosY != min_y:
                game_array[gameArrayPosX+1] = 0x00 # remove cursor
                cursorPosY -= 1
                gameArrayPosY -= 1
       
        # Left
        if Encoder1.position > 0:
            Encoder1.position = 0
            if cursorPosX != min_x:
                game_array[gameArrayPosX+1] = 0x00 # remove cursor
                cursorPosX -= 2
                gameArrayPosX += 2
        
        # Right
        elif Encoder1.position < 0:
            Encoder1.position = 0
            if cursorPosX != max_x - 2:
                game_array[gameArrayPosX+1] = 0x00 # remove cursor
                cursorPosX += 2
                gameArrayPosX -= 2
        
        time.sleep(.25) # used for debouncing
        
        game_array[gameArrayPosX+1] = game_array[gameArrayPosX+1] | (1 << gameArrayPosY) # add in the cursor
        bus.write_i2c_block_data(matrix, 0, game_array)
        game.move(cursorPosY, cursorPosX)
        game.refresh()
        
    # game complete
    game.erase()
    game.refresh()
    del game

# This function clears the window and makes the boarder
# win - the game window
# height - # of rows
# width - # of columns
def createBoarder(win, height, width):
    win.clear()
    
    # put a board around the edge to know the boundaries
    win.border(1, '|', 1, '-', 1, '+', '+', '+')
    
    # print top 
    for i in range(0, width):
        win.addstr(0, (2*(i+2)) - 1, str(i))

    # print left
    for i in range(0, height):
        win.addstr(i+1, 0, str(i) + ":")

    win.refresh()

# the main function that starts the initialization and clean up
# stdscr - the standard window
def main(stdscr):
    global game_array
    
    # -- INIT -- #
    initCurses(stdscr)
    
    # -- BUTTONS -- #
    GPIO.setup(CLEAR_BUTTON, GPIO.IN)
    GPIO.setup(EXIT_BUTTON, GPIO.IN)
    
    # -- ENCODER -- #
    Encoder1.setAbsolute()
    Encoder1.enable()
    Encoder2.setAbsolute()
    Encoder2.enable()
    
    # -- I2C -- #
    bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
    bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
    bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)
    bus.write_i2c_block_data(matrix, 0, game_array) # clear matrix

    length, width = makeMenu()

    createGameWindow(length, width, stdscr)

    # -- EXIT -- #
    game_array = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ]
    bus.write_i2c_block_data(matrix, 0, game_array)
    
    GPIO.cleanup()
    
    exitCurses(stdscr)

if __name__ == "__main__":
    # this is for debugging with ncurses
    wrapper(main)
