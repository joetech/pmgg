#!/usr/bin/python

from time import gmtime, strftime, sleep
import subprocess
import gmail 
import os
import RPi.GPIO as GPIO
import curses


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

def updateHead(txt):
    win.addstr(0, 1, '                                       ')
    win.addstr(0, 1, txt, curses.COLOR_RED)
    win.refresh()

def updateStat(txt):
    win.addstr(1, 1, txt, curses.A_REVERSE)
    win.refresh()

def clearStat():
    win.addstr(1, 1, '                                       ')
    win.addstr(1, 1, '')
    win.refresh()

headerText = "S to Speak | X to exit"
updateHead(headerText)
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
    updateHead('You said: '+out)
    updateStat('')
    
    if out == 'later':
        updateStat('exit')
        sleep(1)
        clearStat()
        return 'exit'
    elif out == 'take a photo':
        sleep(1)
        headerText = 'Smile while I take your picture'
        updateHead(headerText)
        timestamp = strftime("%Y%m%d%H%M%S", gmtime())
	command = './image.sh'# ' + timestamp
	logEvent('EXEC - ' + command)
        p = subprocess.Popen([command, ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        updateStat('*CLICK*')
        out, err = p.communicate()
        out = out.strip(' \t\n\r')
        sleep(1)
        clearStat()
    elif out == 'menu':
        sleep(1)
        headerText = 'Commands:\nmenu: This menu\ntweet: Send a tweet\ncheck email: Retrieve new emails\ntake a photo: Takes a photo\nlater: Exits the HUD'
    elif out == 'check email':
        sleep(1)
        headerText = 'One moment while I fetch new email'
        updateHead(headerText)
        getMail()
    elif out == 'tweet':
        sleep(1)
        headerText = 'Go ahead... (10 seconds)'
        updateHead(headerText)
        updateStat('talk')
        tweetMsg()
        clearStat()
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
spinnerThrob = [
'.',
'o',
'0',
'o']
spinnerStar = [
'-',
'\\',
'|',
'+',
'/',
'+']

def spinner(spinnerChars):
	for ch in spinnerChars:
		win.move(0,0)
		win.addstr(ch)
		win.refresh()
		sleep(.3)

# Initialize Gmail
g = initEmail()

# Begin main loop
exit = 'nope'
while exit != 'exit':
    buttonStatus = GPIO.input(17)
    if buttonStatus == False:
        updateStat('talk')
        logEvent('Button pressed')
        exit = voiceCommand()
    sleep(0.1)

curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
