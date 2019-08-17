#!/bin/bash

###############################################################################
#    Author: Michael Frohlich
#      Date: 2019
# Copyright: 2019 Michael Frohlich - Modified BSD License
###############################################################################

sudo apt install unclutter
sudo cp kiosk.service /lib/systemd/system/kiosk.service
sudo systemctl enable kiosk.service
sudo systemctl start kiosk.service
