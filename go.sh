#!/bin/sh

# First set the font to something easier to see in the HUD
setfont /usr/share/consolefonts/Lat15-TerminusBold20x10.psf.gz

# Now start the video underlay
#./preview.sh

# Finally, we start up the hud
sudo python ./hud.py
