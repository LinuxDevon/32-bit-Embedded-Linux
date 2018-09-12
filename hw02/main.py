#!/usr/bin/env python3
import curses
import time
from curses import wrapper
import Adafruit_BBIO.GPIO as GPIO

# -- GLOBALS -- #
LEFT_BUTTON =  "P9_42"
RIGHT_BUTTON = "P9_27"
UP_BUTTON = "P9_25"
DOWN_BUTTON = "P9_23"
#CLEAR_BUTTON = "P9_15"

min_x = 3; min_y = 1;
max_x = 50; max_y = 50; # these are arbitrary for now incase of button clicks

# start cursor at top right corner
cursorPosX = min_x; cursorPosY = min_y;
game = None

# keep track of last time a button was pressed
lastButtonTime = None

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
    menu.addstr(3, 0, "Use the 'w' to move up, 's' to move down, 'a' to move left, and 'd' to move right.")
    menu.addstr(5, 0, "'e' is exit the game and 'c' clears the board.")
    menu.addstr(7, int(width / 4), "press any key to continue...");
    
    # update the window
    menu.refresh()

    # wait for user input
    menu.getch()

    # clear the screen to get how big of a board
    menu.clear()
    curses.echo() # show the input

    # ask user how big of a board
    menu.addstr(0, 0, "How wide of a board do you want?")
    menu.refresh()
    
    # Get the input from user for the width
    while True:
         # using try catch to catch non integer inputs
        try:
            width = menu.getstr()
            # check the bounds aren't too small or too big
            if int(width) >= 2 and int(width) <= int((curses.COLS / 2) - 3):
                break
        except:
            menu.clear()
            menu.addstr(0, 0, "Invalid number... values 2 - " + str(int((curses.COLS / 2) - 3)) + ". please enter another number.")
            menu.refresh()

    #clear old text
    menu.clear()

    menu.addstr(0, 0, "How long of a board do you want?")
    menu.refresh()
    
    # Get the input from the user for the length
    while True:
        # using try catch to catch non integer inputs
        try:
            length = menu.getstr()
            # check the bounds aren't too small or too big
            if int(length) > 2 and int(length) <= (curses.LINES - 2):
                break
        except:
            menu.clear()
            menu.refresh()
            menu.addstr(0, 0, "Invalid number... values 2 - " + str(curses.LINES - 2) + ". please enter another number")
    
    # Delete the menu window
    menu.erase()
    menu.refresh()
    del menu
    return int(length), int(width) 
    
# This is the function callback for button presses.
# channel - the button pressed
def readButton(channel):
    global  cursorPosX, cursorPosY, game
    
    game.addstr(cursorPosY, cursorPosX, "X")
    # Down
    if channel == DOWN_BUTTON:
        if cursorPosY != (max_y - 2):
            cursorPosY += 1
    
    # Up
    elif channel == UP_BUTTON:
        if cursorPosY != min_y:
            cursorPosY -= 1
    
    # Left
    elif channel == LEFT_BUTTON:
        if cursorPosX != min_x:
            cursorPosX -= 2
    
    # Right
    elif channel == RIGHT_BUTTON:
        if cursorPosX != max_x - 2:
            cursorPosX += 2
    
    # clear
    elif channel == CLEAR_BUTTON:
        createBoarder(game, height, width)
            
    game.move(cursorPosY, cursorPosX)
    game.refresh()
    #time.sleep(.5) # put this in to prevent double clicks from bad clicks
    
# Make the game window and run the game code
# height - the # of rows
# width - the # of columns
# stdscr - the terminal window
def createGameWindow(height, width, stdscr):
    global min_y, min_x, cursorPosX, cursorPosY, game, max_y, max_x
    
    begin_x = 0; begin_y = 0;
    
    # bounds of the game board
    max_y = height+2; max_x = (2*width)+3;

    # create the gamec window
    game = curses.newwin(max_y, max_x, begin_y, begin_x)

    createBoarder(game, height, width)

    # move default cursor position
    game.move(cursorPosY, cursorPosX)

    # verify that keys don't get echoed
    curses.noecho()
    
    # add the event to detect which button is pressed. Also have it have bouncetime to prevent multiple clicks by accident.
    GPIO.add_event_detect(LEFT_BUTTON, GPIO.RISING, callback=readButton, bouncetime = 250)
    GPIO.add_event_detect(RIGHT_BUTTON, GPIO.RISING, callback=readButton, bouncetime = 250)
    GPIO.add_event_detect(UP_BUTTON, GPIO.RISING, callback=readButton, bouncetime = 250)
    GPIO.add_event_detect(DOWN_BUTTON, GPIO.RISING, callback=readButton, bouncetime = 250)
    #GPIO.add_event_detect(CLEAR_BUTTON, GPIO.RISING, callback=readButton, bouncetime = 250)
    
    # -- GAME LOOP -- #
    while True:
        button = game.getch()
        game.addstr(cursorPosY, cursorPosX, "X")
        
        # Down
        if button == ord('s'):
            if cursorPosY != (max_y - 2):
                cursorPosY += 1

        # Up
        elif button == ord('w'):
            if cursorPosY != min_y:
                cursorPosY -= 1
       
       # Left
        elif button == ord('a'):
            if cursorPosX != min_x:
                cursorPosX -= 2
        
        # Right
        elif button == ord('d'):
            if cursorPosX != max_x - 2:
                cursorPosX += 2
        
        # clear
        elif button == ord('c'):
            createBoarder(game, height, width)
            
        # close
        elif button == ord('e'):
            break
        
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
    # -- INIT -- #
    initCurses(stdscr)
    
    # -- LED/GPIO -- #
    GPIO.setup(LEFT_BUTTON, GPIO.IN)
    GPIO.setup(RIGHT_BUTTON, GPIO.IN)
    GPIO.setup(UP_BUTTON, GPIO.IN)
    GPIO.setup(DOWN_BUTTON, GPIO.IN)
    #GPIO.setup(CLEAR_BUTTON, GPIO.IN)

    length, width = makeMenu()

    createGameWindow(length, width, stdscr)

    # -- EXIT -- #
    exitCurses(stdscr)

if __name__ == "__main__":
    # this is for debugging with ncurses
    wrapper(main)
