#!/usr/bin/python

from time import gmtime, strftime
import urwid
import urwid.raw_display
import time
import subprocess
import gmail 

def main():
    text_header = (u"S to Speak | X to exit")
    g = 0

    def button_press(button):
        frame.footer = urwid.AttrWrap(urwid.Text(
            [u"Pressed: ", button.get_label()]), 'header')

    blank = urwid.Divider()
    listbox_content = [
        blank
        ]

    header = urwid.AttrWrap(urwid.Text(text_header), 'header')
    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
    frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)

    palette = [
        ('body','white','black', 'standout'),
        ('reverse','light gray','black'),
        ('footer','white','black', 'bold'),
        ('header','white','dark blue', 'bold'),
        ('working','white','dark red', 'bold'),
        ('important','dark blue','light gray',('standout','underline')),
        ('editfc','white', 'dark blue', 'bold'),
        ('editbx','light gray', 'dark blue'),
        ('editcp','black','light gray', 'standout'),
        ('bright','dark gray','light gray', ('bold','standout')),
        ('buttn','black','dark cyan'),
        ('buttnf','white','dark blue','bold'),
        ]


    screen = urwid.raw_display.Screen()
    
    def voiceCommand():
        frame.footer = urwid.AttrWrap(urwid.Text('Listening...'), 'working')
        p = subprocess.Popen(["./speech.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.strip(' \t\n\r')
        logEvent('VOICE - ' + out)
        frame.footer = urwid.AttrWrap(urwid.Text(out), 'footer')
	if out == 'later':
            raise urwid.ExitMainLoop()
	elif out == 'take a photo':
            time.sleep(1)
            frame.footer = urwid.AttrWrap(urwid.Text('Smile while I take your picture'), 'footer')
            p = subprocess.Popen(["./image.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            out = out.strip(' \t\n\r')
	elif out == 'menu':
            time.sleep(1)
            frame.footer = urwid.AttrWrap(urwid.Text('Commands:\nmenu: This menu\ntweet: Send a tweet\ncheck email: Retrieve new emails\ntake a photo: Takes a photo\nlater: Exits the HUD'), 'footer')
	elif out == 'check email':
            time.sleep(1)
            frame.footer = urwid.AttrWrap(urwid.Text('One moment while I fetch new email'), 'footer')
            getMail()
            # Now call the method to take a photo
	elif out == 'tweet':
            time.sleep(1)
            frame.footer = urwid.AttrWrap(urwid.Text('Go ahead...'), 'footer')
            tweetMsg()
            # Now call the method to take a photo

    def tweetMsg():
        p = subprocess.Popen(["./speech-long.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.strip(' \t\n\r')
        time.sleep(1)
        frame.footer = urwid.AttrWrap(urwid.Text('I heard ' + out + '.  Confirm by saying Send.'), 'footer')
        
    def logEvent(txt):
        f = open('log.txt', 'a')
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        f.write(timestamp + ' - ' + txt + "\n")
        f.close()
        
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
            frame.footer = urwid.AttrWrap(urwid.Text(inbox_txt), 'footer')

    def unhandled(key):
        if key == 'x':
            raise urwid.ExitMainLoop()
        if key == 's':
            voiceCommand()
    
    g = initEmail()

    urwid.MainLoop(frame, palette, screen,
        unhandled_input=unhandled).run()

def setup():
    main()

if '__main__'==__name__ or urwid.web_display.is_web_request():
    setup()
