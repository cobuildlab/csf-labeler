#!/bin/bash
echo "Starting Setup"
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install -y git supervisor python3
# Some versions of ubuntu have a dependecy problem for "build-essential" dependencies
# sudo apt install libc6=2.35-0ubuntu3 libc-bin=2.35-0ubuntu3
sudo apt install -y build-essential python3-pip python3-dev python3-venv libcups2-dev
sudo apt install -y apt-transport-https python3-lgpio python3-rpi.gpio python3-gpiozero
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
sudo apt install -y libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
sudo apt install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good

# Kivy
sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get update
sudo apt-get install -y python3-kivy


# VENV
python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt

#  conf files
sudo cp ./etc/csf-labeler.conf /etc/supervisor/conf.d/
sudo cp ./etc/csf-labeler.rules /etc/udev/rules.d/