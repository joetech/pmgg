#!/bin/sh
#raspistill -q 100 -p 800,500,640,480 -v -op 100 -tl 500 -w 640 -h 480 -o test.jpg
raspistill -q 100 -v -op 100 -t 15000 -o test.jpg

