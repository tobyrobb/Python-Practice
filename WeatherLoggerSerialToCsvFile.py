#python csv file logger for arduino
'''
TODO

read serial csv

split off serial header text and footer text

strip out values

create a dictionary for names and values

create a timestamp

write out the names and values and timestamp to formatted dictionary

write out the formatted dictionary to disk file

advanced optional: publish to a view model

'''


#begin

import time
import serial
import csv


#define variables

comPort = 'COM7'
sleepTime = 10  #seconds of sleep between readings

#define dictionaries

weatherDict = {'Timestamp': '0','Pressure': '0', 'Temperature': '0', 'Humidity': '0', 'Dewpoint': '0', 'Light': '0'}
commaPos = [0,0,0,0,0]

#intialize ports

ser = serial.Serial(
    port= comPort,\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
time.sleep(3)

print("connected to: " + ser.portstr)
print("Welcome to an arduino Serial port reader")
print()
print()


try:
    while True:
            
        #read serial to line list with timestamp

        serialByte = ser.readline()
        serialString = str(serialByte)  # change it to a string from the serial port byte

        print("String received",serialByte)
   
        stringLength = len(serialString)
        print("There are",stringLength, "characters in the string")


        # maybe i should keep a list of the comma positions?

        index = 0
        previousIndex = 0

        try:
            while index < stringLength:
                if serialString.find(",", previousIndex, stringLength) == -1:
                    print("No more commas found")
                    print()
                    break
                commaPos[index] = serialString.find(",", previousIndex, stringLength)
                previousIndex = (commaPos[index] + 1)  
                print("There is a comma at position",commaPos[index])
                index+=1

        except :
            pass

        print()
        print()
        print()
        print()
        print()

        #read values from one comma to another then publish values and timestamp to dictionary

        weatherDict["Timestamp"] = time.strftime("%H:%M:%S")                  #add a timestamp to the dictionary
        weatherDict["Pressure"] = serialString[commaPos[0]+1:commaPos[1]]
        weatherDict["Temperature"] = serialString[commaPos[1]+1:commaPos[2]]
        weatherDict["Humidity"] = serialString[commaPos[2]+1:commaPos[3]]
        weatherDict["Dewpoint"] = serialString[commaPos[3]+1:commaPos[4]]

        lightserialString = serialString[commaPos[4]+1:-1]
        lightserialString = (lightserialString.replace("r", ""))    #remove newline
        lightserialString = (lightserialString.replace("n", ""))
        lightserialString = (lightserialString.replace("\\", ""))
        weatherDict["Light"] = lightserialString


        #publish disk model

        diskFile = open("weatherData.txt", "a")
        diskFile.write("Timestamp")
        diskFile.write(",")
        diskFile.write(weatherDict["Timestamp"])
        diskFile.write(",")
        diskFile.write("Pressure")
        diskFile.write(",")
        diskFile.write(weatherDict["Pressure"])
        diskFile.write(",")
        diskFile.write("Temperature")
        diskFile.write(",")
        diskFile.write(weatherDict["Temperature"])
        diskFile.write(",")
        diskFile.write("Humidity")
        diskFile.write(",")
        diskFile.write(weatherDict["Humidity"])
        diskFile.write(",")
        diskFile.write("Dewpoint")
        diskFile.write(",")
        diskFile.write(weatherDict["Dewpoint"])
        diskFile.write(",")
        diskFile.write("Light")
        diskFile.write(",")
        diskFile.write(weatherDict["Light"])
        diskFile.write("\n")

        diskFile.close()


        #publish view model
        
        print("Weather data at timestamp",weatherDict["Timestamp"])
        print()

        print("Pressure in HectoPascal's               :", weatherDict['Pressure'])
        print("Temperature in Celcius                  :", weatherDict['Temperature'])
        print("Humidity in relative percent            :", weatherDict['Humidity'])
        print("Dewpoint temperature in Celcius         :", weatherDict['Dewpoint'])
        print("Light level relative between 0 and 1023 :", weatherDict['Light'])
        print()
        print("Time between samples is curently",sleepTime,"seconds")
        print()
        print("Control - C to EXIT")
        print()
        print()
        print()
        print()
        print()
        
        time.sleep(sleepTime)   #wait in between readings

except KeyboardInterrupt:
    print()
    print()
    print()
    print()
    print("interrupted! - SHUTTING DOWN")
    print()
    print()
    print()
    print()

    #close everything
    ser.close()
    time.sleep(3)
    exit

