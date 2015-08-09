# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 22:40:22 2015

SpotPriceGet  0.3

This is a python3 program that will fetch electricity spot prices from Nordpool
and save the data to a file. It is intended to be used in conjunction with
another program(s) for controlling electricity usage. It is associated with a
configuration file from which the settings are read. User is advised to observe
the terms and conditions of Nordpool, their website and data. 


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
import sys, requests, json, configparser, datetime

# Get current time and start a log line
currentTime = datetime.datetime.now()
logLine = []
logLine.append(str (currentTime) + ' SPG: ')

#A method for writing the log file
def WriteLog(logLine, logFile = 'log.txt',logState = 'on'):       
    logLine.append('\n')
    logLine = ''.join(logLine)
    #print (logLine)
    if logState == 'on':
        with open(logFile, "a") as fol:
            fol.write(logLine)
    sys.exit()


try:
    # Read settings from a file
    config = configparser.ConfigParser()
    config.read(configFile)
    
    # Get settings *********************************** hardcoded stuff 
    priceURL = config['Settings']['URL'] 
    outputFile = config['Settings']['OutputFile']
    outputType = config['Settings']['OutputType']
    logState = config['Settings']['Log']
    logFile = config['Settings']['LogFile']
    logPrice = config['Settings']['LogPrice']
    userTimeZone = config['Settings']['TimeZone']
    
    
except:
    logLine.append ('Error in reading configuration file. ')
    WriteLog(logLine)
   
# Get prices from URL and parse json, then save prices to list
try:
    pricePage = requests.get(priceURL)
except:
    logLine.append ('Error in fetching data from server. ')
    WriteLog(logLine,logFile, logState )


try:
    parsedPrices = json.loads(pricePage.text)
    
    priceList =[]
    hours =[]
    priceListToday = []
    priceListYesterday = []
    
    for i in range(0,24):
        #****************************** more hardcoded stuff
        priceListToday.append(parsedPrices['data']['Rows'][i]['Columns'][0]['Value'])
        priceListYesterday.append(parsedPrices['data']['Rows'][i]['Columns'][1]['Value'])
        hours.append(i)
except:
    logLine.append ('Error in parsing the data. ')
    WriteLog(logLine,logFile, logState )


#Time zone correction
if userTimeZone == '1':
    priceList.extend(priceListToday)
    
elif userTimeZone == '2':
    priceList.extend(priceListYesterday[-1:])
    priceList.extend(priceListToday[:-1])
    
else:
    logLine.append ('Unsupported timezone! ')

# Generate output, depending on settings,
# option 'p' = write prices to file
# option 'l' = write levels to file, e.g. cheapest is 1, rest 2
# ************************ control setting keys hardcoded

outputStr = []
if outputType == 'p':
    for i in range(0,24):
        outputStr.append(str(hours[i]) + ':' + priceList[i] + '\n' )

# sort prices to levels
elif outputType == 'l':
    #get level values from the config file
    try:    
        levels = []
        for i in range(1,25):
            levels.append(config['Settings']['Level' + str(i)])    
    except:
        logLine.append ('Error in reading level values. ')
        WriteLog(logLine,logFile, logState )

    
    
    priceFloat = []
    for i in priceList:
        priceFloat.append(float(i.replace(',','.')))
    
    outputTmp = [None]*24
    for i in levels:
        priceMaxIndex = priceFloat.index(max(priceFloat))
        outputTmp[priceMaxIndex] = i
        priceFloat[priceMaxIndex] = 0

    for i in range(0,24):
        outputStr.append(str(hours[i]) + ':' + outputTmp[i] + '\n' )

else:
    logLine.append ('NO correct output filetype! ')

try:
    #Write the output to file, first make it a string
    outputStr = ''.join(outputStr)
    with open(outputFile, "w") as fo:
        fo.write(outputStr)
except:
    logLine.append ('Error in writing output file. ')
    WriteLog(logLine,logFile, logState )


#append log with the type of output and optionally with prices 
logLine.append( "'" + outputType  + "' OK. ")
if logPrice == 'on':     
    logLine.append( ' '.join(priceList))


# Finish by writing the a line to the log file if log in 'on' 
WriteLog(logLine,logFile, logState )

# END OF PROGRAM   