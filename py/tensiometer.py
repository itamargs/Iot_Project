#!/usr/bin/python
#-*- coding: utf-8 -*-



from abc import ABC, abstractmethod

class tensiometer(ABC):

    Type = "Tensiometer"
    dataType = "text"

    @abstractmethod
    def getHumidity(self, ):
        pass

    @abstractmethod
    def needToClean(self, ):
        pass


    def getDataType(self):
        return "text"

    def printMyType(self):
        print("Device type: Tensiometer")

