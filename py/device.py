#!/usr/bin/python
#-*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class device(ABC):



    def __init__(self, interval, ID, description):
        self.interval = interval
        self.ID = ID
        self.description = description
        self.dataType = "my data type"
        print("\ninit device:", description)


    @abstractmethod
    def setInterval(self, interval):   # interval for heart beat send
        pass

    @abstractmethod
    def compress(self):  #   generic compression method by the data type of the device
        pass


    # @abstractmethod
    # def getData(self): # get data from sensor
    #     pass

    def sendData(self): # send data to cloud
        pass

    def getReady(self):   # final initializaion of device
        print("Getting ready...\n" )
        self.getData()  #get data from device (data depends on device type)
        self.getSettings() #get settings from device (settings depends on device type)
        self.analyze() # insert values from sensor uoutput into device data members

        # check connection to sensor
        # get data from sensor
        # analyze data from sensor
        # connect to cloud
        pass

    def pulseBroadCast(self): # pulse heart beat to the server
        pass

    def isReady(self, false): #is the device ready to send data amd etc?
        pass

    def createData(self, dataType): #create the data file
        pass

    def setDescription(self, description): # set a new (textual) description to the device
        pass


    def printDetails(self):
        print("ID:", self.ID)
        print("Interval:", self.interval)
        print("Description:", self.description)
        print("Data Type:", self.dataType)

