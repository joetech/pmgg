#!/bin/sh
#raspistill -q 100 -p 800,500,640,480 -v -op 100 -tl 500 -w 640 -h 480 -o test.jpg
raspivid -t 60000 -op 125 -f > /dev/null &
#raspistill -t 0 -o test.jpg
