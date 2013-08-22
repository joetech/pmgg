#!/usr/bin/python

import curses
from time import sleep
stdscr = curses.initscr() # Init the screen
curses.noecho() # Do not echo out keys pressed
curses.cbreak() # Capture keys without requiring the ENTER key
stdscr.keypad(1) # Capture cursor keys

begin_x = 0
begin_y = 0
height = 5
width = 40
win = curses.newwin(height, width, begin_y, begin_x)
sleep(1)

def spinner():
	spinnerChars = ['-','\\','|','/']
	for ch in spinnerChars:
		win.addch(ch)
		win.refresh()
		sleep(.1)

for i in range(1,10):
	spinner()

# headPad = curses.newpad(100, 100)

# def spinner():
# 	spinnerChars = ['-','\\','|','/']
# 	for ch in spinnerChars:
# 		headPad.addch(ch)
# 		headPad.refresh( 0,0, 5,5, 20,110)
# 		sleep(.1)

# for i in range(1,10):
# 	spinner()

# The next 4 lines are cleanup and shutdown
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
