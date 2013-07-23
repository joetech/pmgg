#!/usr/bin/python

import urwid
import urwid.raw_display
import time
import subprocess

def main():
    text_header = (u"Bitches love HUDs!")

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
        ('header','white','dark red', 'bold'),
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
        p = subprocess.Popen(["./speech.sh", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.strip(' \t\n\r')
        frame.header = urwid.AttrWrap(urwid.Text(out), 'header')
	if out == 'take a photo':
            time.sleep(1)
            frame.header = urwid.AttrWrap(urwid.Text('Smile while I take your picture'), 'header')
            # Now call the method to take a photo
	if out == 'check email':
            time.sleep(1)
            frame.header = urwid.AttrWrap(urwid.Text('One moment while I fetch new email'), 'header')
            # Now call the method to take a photo
	if out == 'tweet':
            time.sleep(1)
            frame.header = urwid.AttrWrap(urwid.Text('Go ahead...'), 'header')
            # Now call the method to take a photo
        #frame.header = urwid.AttrWrap(urwid.Text('Recording....'), 'header')
        #time.sleep(1)
        #for i in range(1,3):
        #    frame.header = urwid.AttrWrap(urwid.Text(str(i)), 'header')
        
    def updateMessage():
        voiceCommand()
        #time.sleep(2)
        #command_file = open('command.txt')
        #new_header = ''
        #for line in command_file:
        #    new_header += line
        #frame.header = urwid.AttrWrap(urwid.Text(new_header), 'header')

    def unhandled(key):
        if key == 'f8':
            raise urwid.ExitMainLoop()
        if key == 'f7':
            updateMessage()
    
    urwid.MainLoop(frame, palette, screen,
        unhandled_input=unhandled).run()

def setup():
    main()

if '__main__'==__name__ or urwid.web_display.is_web_request():
    setup()
