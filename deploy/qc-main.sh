#!/bin/bash

###############################################################################
#    Author: Michael Frohlich
#      Date: 2019
# Copyright: 2019 Michael Frohlich - Modified BSD License
###############################################################################

sudo xset s off
sudo xset -dpms
sudo xset s noblank
sudo unclutter -idle 0 &

sleep 10

cd /home/pi/workspace/qc16_bases
git pull

sleep 1

cd /home/pi/workspace/qc16_bases/ReactApp/
node server.js &

export PYTHONPATH="/home/pi/workspace/qc16_bases:"
cd /home/pi/workspace/qc16_bases/PythonApp/
source /home/pi/workspace/qc16_bases/PythonApp/venv/bin/activate
python /home/pi/workspace/qc16_bases/PythonApp/MessageQueueReceiverMain.py &
sleep 2
python /home/pi/workspace/qc16_bases/PythonApp/main.py &

/usr/bin/chromium-browser --kiosk --app=http://localhost:8090/react/

