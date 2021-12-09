#!/bin/bash

# Updating setuptools and pip
echo 'Installing package updates [setuptools] [pip] [wheel]'
sudo pip3 install --upgrade pip
sudo pip3 install --upgrade setuptools
sudo pip3 install --upgrade wheel

# Install all the necessary python3 packages
echo 'Installing package [screeninfo] ...'
sudo pip3 install screeninfo

echo 'Installing package [tweepy] ...'
sudo pip3 install tweepy

echo 'Installing package [cv2] ...'
sudo pip3 install opencv-python
