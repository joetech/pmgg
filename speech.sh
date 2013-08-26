#!/bin/bash
#echo "Recording... Press Ctrl+C to Stop."
arecord -D "hw:0,0" -f S16_LE -d 2 -r 44100 test.wav > /dev/null 2>&1
ffmpeg -y -i test.wav -ar 44100 -acodec flac file.flac > /dev/null 2>&1

#echo "Processing..."
wget -U "Mozilla/5.0" --post-file file.flac --header "Content-Type: audio/x-flac; rate=44100" "http://www.google.com/speech-api/v1/recognize?lang=en-us&client=chromium" > /dev/null 2>&1
mv "recognize?lang=en-us&client=chromium" stt.txt
cut -d "\"" -f12 stt.txt > command.txt

cat command.txt

rm file.flac > /dev/null 2>&1
rm test.wav > /dev/null 2>&1
