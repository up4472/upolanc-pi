#!/bin/bash

#
# To run this file on reboot add the following line to crontab (sudo crontab -e) :
# @reboot sh /home/pi/upolanc-pi/launcher.py >/home/pi/upolanc-pi/logs/cronlog 2>&1
#

clear

cd /home/pi/upolanc-pi/

sudo python3 app.py

cd ..
