#!/usr/bin/python
# -*- coding: utf-8 -*-
# interface
# import this to you class so it can be a device
# all methods with "@abstractmethod" decorators are MUST be implementer into the sub class of this.
# please copy the comment "override from ***"  to the subclass to make the code more readable
# if method is NOT abstract,then the operation of this method isn't unique to the specific device type.
# example for abstract:  "setInterval()" ALL type of devices  has interval need to be set but exact interval is depends on device type
# example for none abstract:  "sendData()" ALL type of devices need to send data to the cloud no matter what is that data
# if method is abstract, then the operation of this method IS unique to the specific device type.
from abc import ABC, abstractmethod
import pickle  # saving object for other sessions
import dill as pickle
import socket
import sys
import os

class device(ABC):

    def __init__(self, interval, ID, description):
        self.interval = interval
        self.ID = 12
        self.description = description
        self.dataType = "my data type"
        print("device: init device:", description)

    def save(self, path):
        with open(path, 'wb') as f:
            return pickle.dump(self, f)

    def load(self, path):
        with open(path, 'rb') as f:
            self.__dict__.update(pickle.load(f).__dict__)

    @abstractmethod
    # override from device
    def setInterval(self, interval):  # interval for heart beat send
        pass

    def compress(self):  # compress data with some known compress method
        print("device: compressing data")
        pass  # todo: place holder. need to write the method

    # override from device
    def doesNeedAnalyzing(
            self):  # is the data need to be analyzed (example: if only 1 second past from last time there is no need)
        print("device: check if need analyze")
        return True  # todo: just place holder, need to check if need analyze

    @abstractmethod
    # override from device
    def deleteOutdatedData(self):  # delete data who isn't nececcery anymore for cleaning space in device memory
        print("device: deleteOutdatedData")
        pass

    def sendData(self):  # send data to cloud
        print("device: sending data")
        pass

    def getReady(self):  # final initializaion of device
        print("device: Getting ready...")
        self.getData()  # get data from device (data depends on device type)
        self.getSettings()  # get settings from device (settings depends on device type)
        self.analyze()  # insert values from sensor uoutput into device data members

        # check connection to sensor
        # get data from sensor
        # analyze data from sensor
        # connect to cloud
        pass

    def isTheDataHasChanged(self):  # boolean
        print("device: Check for change in data...")
        return self.compareData()  # compare the new data from the sensor to the data captured last time. (return true if data has changed)

    def getChange(self):  # get the change from the old data that captured in sensor to the new data captured
        print("device: get the change in data...")
        # todo: place holder. need to write the method

        # check connection to sensor
        # get data from sensor
        # analyze data from sensor
        # connect to cloud
        pass

    def sendPulse(self):  # pulse heart beat to the server
        print("device: sending pulse")
        pass

    def isReady(self, false):  # is the device ready to send data amd etc?
        pass

    def createData(self, dataType):  # create the data file
        pass

    def setDescription(self, description):  # set a new (textual) description to the device
        pass

    def sdeleteOutDatedData(self):
        pass  # todo: place holder. need to write the method

    def sendData(fileName):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port  = 5002
        sock.connect((host, port))
        # file_name, file_extension = os.path.splitext(fileName)
        # print(file_name)
        # print(file_extension)
        # sock.sendmsg(file_name)

        with open(fileName, 'rb') as f:
            data = f.read()
            sock.sendall(data)


        sock.close()
        f.close()




    sendData('sample.wav')



    def printDetails(self):
        print("ID:", self.ID)
        print("Interval:", self.interval)
        print("Description:", self.description)
        print("Data Type:", self.dataType)
