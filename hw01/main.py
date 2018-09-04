#!/usr/bin/env python3
import curses
from curses import wrapper

def initCurses(stdscr):
    # Allow keystroke reading
    curses.noecho()

    # turn off buffered input
    curses.cbreak()

    # Enable arrow keys
    stdscr.keypad(True)

def exitCurses(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def makeMenu():
    begin_x = 0; begin_y = 0;
    height = curses.LINES; width = curses.COLS;

    # create the menu window
    menu = curses.newwin(height, width, begin_y, begin_x)
    
    # add the letters to the window
    menu.addstr(0, int(width / 2), "Etch A Sketch",curses.A_BLINK)
    menu.addstr(1, int(width / 4), "Use the arrow keys to navigate the on the screen. Where you go leaves an X in its place. Hit 'Backspace' to erase the screen. Hit 'shift' or 'e' to exit.")
    menu.addstr(5, int(width / 4), "press any key to continue...");
    
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
    width = menu.getstr()
    while int(width) < 2 or int(width) >= (curses.COLS - 1):
        menu.clear()
        menu.addstr(0, 0, "Invalid number... values 2 - " + str(curses.COLS) + ". please enter another number.")
        menu.refresh()
        width = menu.getstr()

    #clear old text
    menu.clear()

    menu.addstr(0, 0, "How long of a board do you want?")
    menu.refresh()
    length = menu.getstr()
    while int(length) < 2 or int(length) >= (curses.LINES - 1):
        menu.clear()
        menu.refresh()
        menu.addstr(0, 0, "Invalid number... values 2 - " + str(curses.LINES) + ". please enter another number")
        length = menu.getstr()
    
    menu.erase()
    menu.refresh()
    del menu
    return int(length), int(width) 

def createGameWindow(height, width, stdscr):
    begin_x = 0; begin_y = 0;
    max_x = height+1; max_y = 2*(width+3);

    cursorPosX = 3; cursorPosY = 1;
    # create the menu window
    game = curses.newwin(max_x, max_y, begin_y, begin_x)

    createBoarder(game, height, width)

    # move default cursor position
    game.move(cursorPosY, cursorPosX)

    curses.noecho()
    #stdscr.keypad(True)
    button = game.getch()

    while True:
        game.addstr(cursorPosY, cursorPosX, "X")
        
        # Bounds Check
        if cursorPosY == max_y or cursorPosX == max_x or cursorPosY < 1 or cursorPosX < 3:
            # do nothing
            continue
        # Down
        if button == ord('s'):
            cursorPosY += 1

        # Up
        elif button == ord('w'):
            cursorPosY -= 1
       
       # Left
        elif button == ord('a'):
            cursorPosX -= 2
        
        # Right
        elif button == ord('d'):
            cursorPosX += 2
        
        game.move(cursorPosY, cursorPosX)
        game.refresh()
        button = game.getch()

def createBoarder(win, height, width):
    win.clear()
    for i in range(0, width):
        win.addstr(0, (2*(i+2)) - 1, str(i))

    for i in range(0, height):
        win.addstr(i+1, 0, str(i) + ":")

    win.refresh()

def main(stdscr):
    # -- INIT -- #
    initCurses(stdscr)

    length, width = makeMenu()

    createGameWindow(length, width, stdscr)

    
    stdscr.getch()
    # -- EXIT -- #
    exitCurses(stdscr)

if __name__ == "__main__":
    wrapper(main)
