#!/bin/bash

#
# To run this file on reboot add the following line to crontab (sudo crontab -e) :
# @reboot sh /home/pi/upolanc-pi/launcher.py >/home/pi/upolanc-pi/logs/cronlog 2>&1
#

clear

cd /home/pi/upolanc-pi/

export PYGAME_HIDE_SUPPORT_PROMPT=1

sudo XAUTHORITY=/home/pi/.Xauthority DISPLAY=:10.0 QT_X11_NO_MITSHM=1 python3 app.py

cd ..
