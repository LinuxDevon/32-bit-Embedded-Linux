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
    menu.addstr(0, width / 2, "Etch A Sketch",curses.A_BLINK)
    menu.addstr(1, width / 4, "Use the arrow keys to navigate the on the screen. Where you go leaves an X in its place. Hit 'Backspace' to erase the screen. Hit 'shift' or 'e' to exit.")
    menu.addstr(5, width / 4, "press any key to continue...");
    
    # update the window
    menu.refresh()

    # wait for user input
    menu.getch()

def main(stdscr):
    # -- INIT -- #
    initCurses(stdscr)

    makeMenu()

    # -- EXIT -- #
    exitCurses(stdscr)

if __name__ == "__main__":
    wrapper(main)
