#!/bin/sh
# First set the font to something easier to see in the HUD
setfont /usr/share/consolefonts/Lat15-TerminusBold20x10.psf.gz

# Now start in the right directory
cd /home/pi/pmgg

# Finally, we start up the hud
sudo python ./hud.py
