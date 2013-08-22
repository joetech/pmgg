#!/usr/bin/python

from time import sleep
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

while True:
	print GPIO.input(17)
        if ( GPIO.input(17) == False ):
		pass
        sleep(0.1);

