# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 22:13:42 2016

TimerHeatPumpControl 0.1

This program will control a heatpump via Thermiq module based on time of day.

Requires python 3.

Author: 
Arttu Huttunen
Oulu, Finland
Created in 2016

/*
 * ----------------------------------------------------------------------------
 * The MIT License (MIT)
 * Copyright (c) 2016 Arttu Huttunen 
 * Anyone is free to do whatever they want with this code, at their own risk.
 * ----------------------------------------------------------------------------
 */

INSTRUCTIONS:
1. Set to run hourly e.g. with cron
2. Set the desired temperature values below in deg Celcius,
'hour00' start at midnight. 

Cron example:
# sudo crontab -e

and edit a line in crontab to:
0 * * * * python3 /home/pi/TimerHeatPumpControl.py

"""
# Set serial port settings:
serialPort = '/dev/ttyUSB0'
serialBaudrate = 9600
serialTimeout = 5


# Set the desired output temperature values here
hour00 = 20
hour01 = 20
hour02 = 20
hour03 = 20
hour04 = 20
hour05 = 20
hour06 = 20
hour07 = 20
hour08 = 20
hour09 = 20
hour10 = 20
hour11 = 20
hour12 = 20
hour13 = 20
hour14 = 20
hour15 = 20
hour16 = 20
hour17 = 20
hour18 = 20
hour19 = 20
hour20 = 20
hour21 = 20
hour22 = 20
hour23 = 20








#**********************************************************
#ACTUAL PROGRAM STARTS HERE, DO NOT EDIT

import datetime, serial

#make list of target temps
targets = [
hour00,
hour01,
hour02,
hour03,
hour04,
hour05,
hour06,
hour07,
hour08,
hour09,
hour10,
hour11,
hour12,
hour13,
hour14,
hour15,
hour16,
hour17,
hour18,
hour19,
hour20,
hour21,
hour22,
hour23]

# Get current time
currentHour = datetime.datetime.now().hour

currentTarget = hex(targets[currentHour])

#create atw command
command = ('atw3200'+currentTarget[2:]+'\n').encode('UTF-8')
print (command)

ser = serial.Serial(
    port = serialPort,
    baudrate = int(serialBaudrate),
    timeout = int(serialTimeout)
    )

ser.write(command)


# END OF PROGRAM