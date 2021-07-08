#!/bin/bash
sudo pigpiod -p 6555
python3 ./pi_cam/main.py
sudo killall pigpiod