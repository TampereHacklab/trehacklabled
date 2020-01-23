#! /bin/bash

# This should run when system boots
# Starts user led display program

#Systemd service called ledmatrix.service handles starting this,
#Stop: sudo systemctl stop ledmatrix.service
#Start: sudo systemctl start ledmatrix.service

#NOT FULLY IMPLEMENTED YET!
/usr/bin/python3 /home/trehacklab/led.py
