#!/usr/bin/python
#-*- coding: utf-8 -*-
# interface
# import this to you class so it can be a device
# all methods with "@abstractmethod" decorators are MUST be implementer into the sub class of this.
# please copy the comment "override from ***"  to the subclass to make the code more readable
# if method is NOT abstract,then the operation of this method isn't unique to the specific device type.
# example for abstract:  "setInterval()" ALL type of devices  has interval need to be set but exact interval is depends on device type
# example for none abstract:  "sendData()" ALL type of devices need to send data to the cloud no matter what is that data
# if method is abstract, then the operation of this method IS unique to the specific device type.
from abc import ABC, abstractmethod


class device(ABC):



    def __init__(self, interval, ID, description):
        self.interval = interval
        self.ID = ID
        self.description = description
        self.dataType = "my data type"
        print("\ninit device:", description)


    @abstractmethod
    #override from device
    def setInterval(self, interval):   # interval for heart beat send
        pass

    @abstractmethod
    #override from device
    def compress(self):  #   generic compression method by the data type of the device
        pass #todo: place holder. need to write the method


    @abstractmethod
    #override from device
    def doesNeedAnalyzing(self):   # is the device need to be analyzed
        pass

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

    def isTheDataHasChanged(self): #boolean
        print("Check for change in data...\n" )
        self.compareData()  #compare the new data from the sensor to the data captured last time

        def getChange(self): #get the change from the old data that captured in sensor to the new data captured
            print("get the change in data...\n")
            #todo: place holder. need to write the method


        # check connection to sensor
        # get data from sensor
        # analyze data from sensor
        # connect to cloud
        pass

    def sendPulse(self):  # pulse heart beat to the server
        pass

    def isReady(self, false):  # is the device ready to send data amd etc?
        pass

    def createData(self, dataType):  # create the data file
        pass

    def setDescription(self, description):  # set a new (textual) description to the device
        pass

    def sdeleteOutDatedData(self):
        pass    #todo: place holder. need to write the method

    def printDetails(self):
        print("ID:", self.ID)
        print("Interval:", self.interval)
        print("Description:", self.description)
        print("Data Type:", self.dataType)

