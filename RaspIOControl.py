# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 23:38:32 2015

RaspIOControl 0.2 (tested)

This is a python3 program that will read a list of commands from a file and
set Raspberry Pi GPIO state accordingly. GPIO mode is BOARD.

Author:
Arttu Huttunen
Oulu, Finland
Created in 2015 

/*
* ----------------------------------------------------------------------------
* The MIT License (MIT)
* Copyright (c) 2015 Arttu Huttunen
* Anyone is free to do whatever they want with this code, at their own risk.
* ----------------------------------------------------------------------------
*/

"""

#config file

configFile = './Settings.txt'

#Actual code starts here
#---------------------------------------------------------------------------

import sys, configparser, datetime, time
import RPi.GPIO as GPIO

# Get current time and start a log line

currentTime = datetime.datetime.now()
logLine = []
logLine.append(str (currentTime) + ' RPC: ')
currentHour = datetime.datetime.now().hour

#A method for writing the log file, default to log.txt
def WriteLog(logLine, logFile = 'log.txt',logState = 'on'):
    logLine.append('\n')
    logLine = ''.join(logLine)
    if logState == 'on':
        with open(logFile, "a") as fol:
            fol.write(logLine)
    sys.exit()

try:
    # Read settings from a file
    config = configparser.ConfigParser()
    config.read(configFile)
 
    # Get settings *********************************** hardcoded stuff
    inputFile = config['Settings']['OutputFile']
    logState = config['Settings']['Log']
    logFile = config['Settings']['LogFile']

    GPIOpin = config['Settings']['GPIOpin']
    GPIOpin = int(GPIOpin)

except:
    logLine.append ('Error in reading configuration file. ')
    WriteLog(logLine)

try:
    commands = {}
    with open(inputFile) as f:
        for line in f:
           (key, val) = line.split(':')
           val = val.rstrip('\n')
           commands[int(key)] = val

except:
    logLine.append ('Error in reading input file. ')
    WriteLog(logLine)

command = commands[currentHour]

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIOpin, GPIO.OUT)
    counter = 0
    if command == 'True':
        logLine.append ('True ')
        while counter < 3000:
            GPIO.output(GPIOpin, True)
            time.sleep(1)
            GPIO.output(GPIOpin, False)
            time.sleep(1)
            counter = counter + 2

    elif command == 'False' :
        logLine.append('False ')
        while counter < 3000:
            GPIO.output(GPIOpin, True)
            time.sleep(1)
            GPIO.output(GPIOpin, False)
            time.sleep(4)
            counter = counter + 5

    else:
        logLine.append ('Stupid command. ')

    GPIO.cleanup()

except:
    logLine.append ('Error in setting GPIO pin. ')
    WriteLog(logLine)

logLine.append('OK.')

WriteLog(logLine,logFile, logState )

 

# END OF PROGRAM