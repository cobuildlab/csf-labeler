#!/bin/bash
git reset --hard
git pull origin main
gnome-terminal --window-with-profile=csf -- python3 /home/cobuild/csf-labeler/app.py -f
