#!/bin/bash
echo "Starting Setup"
sudo apt install -y git supervisor build-essential python3 python3-pip python3-dev apt-transport-https python3-lgpio python3-rpi.gpio python3-gpiozero
sudo apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
sudo apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good

sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get update
sudo apt-get install python3-kivy

python3 -m pip install --upgrade evdev
python3 -m pip install --upgrade pyusb
python3 -m pip install --upgrade qrcode
python3 -m pip install --upgrade Pillow
python3 -m pip install -r requirements.txt

sudo cp ./etc/labeler.conf /etc/supervisor/conf.d/





