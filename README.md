# Poor Man's Google Glass (PMGG)


## Author

* Joe Colburn (https://github.com/joetech) (http://www.joetech.com)


## Thanks
* Karl Herrick for his guidance
* GMail for Python (https://github.com/charlierguo/gmail)


## Hardware needed

* Vuzix iWear AV310 HMD (~$60-$100) - There are similar off-brands, but I used Vuzix
* Raspberry Pi Model B ($35)
* Raspberry Pi case ($12)
* Raspberry Pi Camera ($35)
* Sabrent USB audio card ($10)
* Audio Technica (or other cheap) microphone ($8)
* Tenda W311M (or other cheap) wireless N adapter ($10)
* Tactile button, 10k resistor, wires (~$1)


## Installation

* Grab the files:
    git clone git://github.com/joetech/pmgg.git
* From inside your new pmgg directory grab the gmail api:
    git clone git://github.com/charlierguo/gmail.git
* Still in your pmgg directory, create a "photos" directory
    mkdir photos
* Update credentials files with your info (to be named later)
* Follow hardware instructions at (URL forthcoming)


## Features

* Check email
* Send and receive tweets
* Get Facebook updates
* Take a photo
* Share a photo
* Get weather updates (coming)


## Basic usage

To start, simply run go.sh.

    ./go.sh
    

## Roadmap
* Clean up the interface a bit
* More documentation
* Facebook/Gmail/Twitter notifications area
* Script to kill image preview, snap the image and restart the preview
* Read an email
* Update to Facebook
* Actually send the tweet with option to review first
* Fix credential management
* More APIs! (now taking suggestions and pull requests)
* Ability to share photos with Facebook/Twitter/Email
* Ability to review photos
* Capture video
* Share video with Vine/Facebook/Twitter
* Learn more Python and clean up this code


## Copyright

* Copyright (c) 2013 Joe Colburn

See LICENSE for details.
