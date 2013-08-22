#!/usr/bin/python

from time import gmtime, strftime, sleep
import subprocess
import gmail 
import os
import RPi.GPIO as GPIO
import curses

    headerText = "S to Speak | X to exit"
    g = 0

    def logEvent(txt):
        f = open('log.txt', 'a')
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        f.write(timestamp + ' - ' + txt + "\n")
        f.close()
        
    def voiceCommand():
        headerText = 'Listening...'
        p = subprocess.Popen(["./speech.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.strip(' \t\n\r')
        logEvent('VOICE - ' + out)
	headerText = out
	if out == 'later':
            return 'exit'
	elif out == 'take a photo':
            sleep(1)
            headerText = 'Smile while I take your picture'
            p = subprocess.Popen(["./image.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            out = out.strip(' \t\n\r')
	elif out == 'menu':
            sleep(1)
            headerText = 'Commands:\nmenu: This menu\ntweet: Send a tweet\ncheck email: Retrieve new emails\ntake a photo: Takes a photo\nlater: Exits the HUD'
	elif out == 'check email':
            sleep(1)
            headerText = 'One moment while I fetch new email'
            getMail()
	elif out == 'tweet':
            sleep(1)
            headerText = 'Go ahead...'
            tweetMsg()
            # Now call the method to take a photo
        return headerText

    def tweetMsg():
        p = subprocess.Popen(["./speech-long.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.strip(' \t\n\r')
        sleep(1)
        headerText = 'I heard ' + out + '.  Confirm by saying Send.'

    def initEmail():
        global g
        f = open('email_creds.txt', 'r')
        line = f.read()
        creds = line.split('|')
        f.close()
        # g = gmail.login(creds[0], creds[1])
        g = gmail.login('pifacetest', 'SuperSecure!')

    def getMail():
        global g
        mail = g.inbox().mail(unread=True)
        inbox_txt = ""
        for msg in mail:
            msg.fetch()
            inbox_txt += msg.fr + msg.subject + "\n"
            headerText = inbox_txt





# Set up the curses window basics
stdscr = curses.initscr() # Init the screen
curses.noecho() # Do not echo out keys pressed
curses.cbreak() # Capture keys without requiring the ENTER key
stdscr.keypad(1) # Capture cursor keys

# Create a new curses window instance
begin_x = 0
begin_y = 0
height = 5
width = 40
win = curses.newwin(height, width, begin_y, begin_x)

# Set up button listener
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

# set up some fun animations
spinnerArrow = [
'      |',
'>     |',
'->    |',
'-->   |',
'--->  |',
'----> |',
' ----)|',
' ---(-|',
' --(--|',
' -(---|',
' <----|',
'<---- |',
'<---- |',
'----  |',
'---   |',
'--    |',
'-     |',
'      |']
spinnerThrob = ['.','o','0','o']
spinnerStar = ['-','\\','|','+','/','+']

def spinner(spinnerChars):
	for ch in spinnerChars:
		win.move(0,0)
		win.addstr(ch)
		win.refresh()
		sleep(.3)

for i in range(1,10):
	spinner(spinnerArrow)

# Initialize Gmail
g = initEmail()

# Begin main loop
while 1==1:
	if GPIO.input(17) == False:
		logEvent('Button pressed')
		voiceCommand()
	# elif GPIO.input(17) == True:
		# logEvent('Open')
	sleep(0.1);

curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
