#!/bin/bash
echo "Starting CSF LABELER..."
pwd
sleep 5
cd /home/cobuild/csf-labeler
pwd
git reset --hard
git pull origin main
#gnome-terminal --window-with-profile=csf -- python3 /home/cobuild/csf-labeler/app.py -f
bash etc/setup.sh
python3 -m venv venvs
source venv/bin/activate
pip3 install -r requirements.txt
pyclean -v .
python3 app.py