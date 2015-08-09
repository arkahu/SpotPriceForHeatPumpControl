# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 23:38:32 2015

HeatPumpControl 0.3

This is a python3 program that will read a list of commands from a file and
will then control a heatpump according to the data. 

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
import sys, configparser, datetime, serial

# Get current time and start a log line
currentTime = datetime.datetime.now()
logLine = []
logLine.append(str (currentTime) + ' HPC: ')
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
    serialPort = config['Settings']['SerialPort']
    serialBaudrate = config['Settings']['Baudrate']
    serialTimeout = config['Settings']['Timeout']

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

#atwxxhhll               Write hhll to register xx
command = commands[currentHour]

try:
    ser = serial.Serial(
        port = serialPort,
        baudrate = int(serialBaudrate),
        timeout = int(serialTimeout)
    )
    ser.write(command,'utf-8')
    ser.close()

except:
    logLine.append ('Error in writing to serial port. ')
    WriteLog(logLine)

# Finish by writing the a line to the log file if log in 'on' 
logLine.append('OK.')
WriteLog(logLine,logFile, logState )

# END OF PROGRAM  