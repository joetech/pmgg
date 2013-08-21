#!/usr/bin/python

import curses
from time import sleep
stdscr = curses.initscr() # Init the screen
curses.noecho() # Do not echo out keys pressed
curses.cbreak() # Capture keys without requiring the ENTER key
stdscr.keypad(1) # Capture cursor keys

#begin_x = 20 ; begin_y = 7
#height = 5 ; width = 40
#win = curses.newwin(height, width, begin_y, begin_x)

pad = curses.newpad(100, 100)
for y in range(0, 100):
    for x in range(0, 100):
        try: pad.addch(y,x, ord('a') + (x*x+y*y) % 26 )
        except curses.error: pass

        # Displays a section of the pad in the middle of the screen
        pad.refresh( 0,0, 5,5, 20,75)
        sleep(.003)

# The next 4 lines are cleanup and shutdown
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
