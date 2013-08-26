#!/usr/bin/python

from time import gmtime, strftime, sleep, mktime
import subprocess
import gmail 
import datetime
import os
import sys
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
height = 10
width = 40
win = curses.newwin(height, width, begin_y, begin_x)

def cursesWrite(y, x, txt, color):
    try:
        win.addstr(y, x, txt, color)
    except curses.error:
        pass

def updateHead(txt):
    cursesWrite(0, 1, '                                       ', 1)
    cursesWrite(0, 1, txt, curses.COLOR_RED)
    win.refresh()

def updateStat(txt):
    clearStat()
    cursesWrite(1, 1, txt, curses.A_REVERSE)
    win.refresh()

def updateNotifications(txt):
    clearNotifications()
    x = 36 - len(txt)
    cursesWrite(1, x, txt, curses.A_REVERSE)
    win.refresh()

def updateBody(txtArr):
    x = 2
    for txt in txtArr:
        cursesWrite(x, 0, '                                       ', 1)
        cursesWrite(x, 1, txt, 1)
        x += 1
    win.refresh()

def updateBodyList(txtArr):
    x = 0
    newArr = []
    for txt in txtArr:
        if txt != '':
            y = x + 3
            cursesWrite(y, 0, '                                       ', 1)
            txt = str(x + 1) + '. ' + txt
            cursesWrite(y, 1, txt, 1)
            x += 1
    win.refresh()

def clearStat():
    cursesWrite(1, 0, '                       ', 1)
    cursesWrite(1, 1, '', 1)
    win.refresh()

def clearNotifications():
    cursesWrite(1, 20, '                  ', 1)
    cursesWrite(1, 20, '', 1)
    win.refresh()

headerText = 'Press button | "menu" for commands'
updateHead(headerText)
cursesWrite(2, 1, '----------------------------------', 1)
g = 0
pid = 99999999
fileList = []

def logEvent(txt):
    f = open('log.txt', 'a')
    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    f.write(timestamp + ' - ' + txt + "\n")
    f.close()

def voiceCommand():
    global pid
    headerText = 'Listening...'
    p = subprocess.Popen(["./speech.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.strip(' \t\n\r')
    logEvent('VOICE - ' + out)
    updateHead('You said: '+out)
    updateStat('')
    
    if (out == 'exit') or (out == "leave") or (out == "please") or (out == "lease") or (out == "leaf"):
        updateStat('exit')
        clearStat()
	logEvent('SYSTEM - Shutting down video preview at pid ' + str(pid))
        os.kill(pid, 9)
        return 'exit'
    elif out == 'update software':
	#command = './update.sh'
	#logEvent('EXEC - ' + command)
	#logEvent('SYSTEM - Updating software from Github ')
        #p = subprocess.Popen([command, ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #out, err = p.communicate()
        #out = out.strip(' \t\n\r')
        headerText = 'PMGG System software updated!'
        updateHead(headerText)
    elif (out == 'take a photo') or (out == 'take a picture'):
        headerText = 'Smile while I take your picture'
        updateHead(headerText)
	command = './image.sh'
	logEvent('EXEC - ' + command)
	logEvent('SYSTEM - Shutting down video preview at pid ' + str(pid))
        os.kill(pid, 9)
        p = subprocess.Popen([command, ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sleep(1)
        pid = preview()
        updateStat('*CLICK*')
        out, err = p.communicate()
        out = out.strip(' \t\n\r')
        sleep(1)
        clearStat()
    elif out == 'list photos':
        fileDir = './photos/'
        fileList = [ f for f in os.listdir(fileDir) if os.path.isfile(os.path.join(fileDir,f)) ]
	logEvent('Listing photos')
        headerText = 'Available photos (say "view photo"):'
        updateHead(headerText)
	updateBodyList(fileList)
        return fileList
    elif (out == 'view photo') or (out == 'view photos'):
        sleep(1)
        headerText = 'Number of the photo to view?'
        updateHead(headerText)
        updateStat('talk')
        photoViewPrompt()
        clearStat()
    elif out == 'list videos':
        fileDir = './videos/'
        fileList = [ f for f in os.listdir(fileDir) if os.path.isfile(os.path.join(fileDir,f)) ]
	logEvent('Listing videos')
        headerText = 'Available videos (say "play video"):'
        updateHead(headerText)
	updateBodyList(fileList)
        return fileList
    elif out == 'play video':
        sleep(1)
        headerText = 'Number of the video to play?'
        updateHead(headerText)
        updateStat('talk')
        videoPlayPrompt()
        clearStat()
    elif out == 'capture video':
        sleep(1)
        headerText = 'Capturing 5 seconds of video'
        updateHead(headerText)
	command = './video.sh'
	logEvent('EXEC - ' + command)
	logEvent('SYSTEM - Shutting down video preview at pid ' + str(pid))
        os.kill(pid, 9)
        p = subprocess.Popen([command, ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.strip(' \t\n\r')
	sleep(1)
        pid = preview()
    elif out == 'menu':
        sleep(1)
        txt = [
        'Commands:',
        'menu: This menu',
        'update software: Updates system software',
        'tweet: Send a tweet',
        'check email: Retrieve new emails',
        'take a photo: Takes a photo',
        'capture video: Captures 5 seconds of video',
        'list videos: Lists captured videos,'
        'leave: Exits the HUD'
        ]
        updateBody(txt)
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

def preview():
    sleep(1)
    logEvent('SYSTEM - Starting video preview overlay')
    try:
        return os.spawnlp(os.P_NOWAIT, 'raspivid', 'raspivid', '-t', '9999999999999', '-op', '125', '-f')
    except Exception, e:
        logEvent('FAILURE - ' + str(e))

def photoViewPrompt():
    global fileList
    global pid
    p = subprocess.Popen(["./speech.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.strip(' \t\n\r')
    sleep(1)
    logEvent('Viewing photo ' + out)
    try:
        pic = int(out)
        pic = pic - 1
        command = ['fbi', '-autodown', '-t', '3', '-1', './photos/' + fileList[pic]]
        logEvent('EXEC - fbi -autodown -t 3 -1 ' + command[5])
	logEvent('SYSTEM - Shutting down video preview at pid ' + str(pid))
        os.kill(pid, 9)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	sleep(8)
        pid = preview()
    except Exception, e:
        logEvent('FAILURE - ' + str(e) + ' - ' + out)
        headerText = 'Sorry.  Try again'
        updateHead(headerText)

def videoPlayPrompt():
    global fileList
    global pid
    p = subprocess.Popen(["./speech.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.strip(' \t\n\r')
    sleep(1)
    logEvent('Playing video ' + out)
    try:
        vid = int(out)
        vid = vid - 1
        command = ['omxplayer', './videos/' + fileList[vid]]
        logEvent('EXEC - omxplayer ' + command[1])
	logEvent('SYSTEM - Shutting down video preview at pid ' + str(pid))
        os.kill(pid, 9)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	sleep(8)
        pid = preview()
    except Exception, e:
        logEvent('FAILURE - ' + str(e) + ' - ' + out)
        headerText = 'Sorry.  Try again'
        updateHead(headerText)

def initEmail():
    logEvent('SYSTEM - Initializing email')
    f = open('email_creds.txt', 'r')
    line = f.read()
    creds = line.split('|')
    f.close()
    # g = gmail.login(creds[0], creds[1])
    return gmail.login('pifacetest', 'SuperSecure!')

def getMail():
    global g
    logEvent('SYSTEM - Fetching email')
    mail = g.inbox().mail(unread=True)
    inbox_txt = ''
    for msg in mail:
        msg.fetch()
        inbox_txt += msg.fr + msg.subject + "||JOE||"
    emailList = inbox_txt.split("||JOE||")
    if len(emailList) > 0:
        updateNotifications('New Mail')
    updateBodyList(emailList)

def checkForEmail(now):
    global g
    logEvent('SYSTEM - Checking for email')
    #mail = g.inbox().mail(unread=True, before=now)
    mail = g.inbox().mail(unread=True)
    inbox_txt = ''
    for msg in mail:
        msg.fetch()
        inbox_txt += msg.fr + msg.subject + "||JOE||"
    emailList = inbox_txt.split("||JOE||")
    if len(emailList) > 0:
        updateNotifications('New Mail')

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

# Begin video overlay
pid = preview()

# Begin main loop
exit = 'nope'
counter = 0
now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
while exit != 'exit':
    buttonStatus = GPIO.input(17)
    if buttonStatus == False:
        updateStat('talk')
        logEvent('Button pressed')
        exit = voiceCommand()
        if isinstance(exit, (list, tuple)):
            fileList = exit
    if counter > 600:
        counter = 0
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        checkForEmail(now)
    counter += 1
    sleep(0.1)

curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
