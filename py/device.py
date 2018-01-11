#!/usr/bin/python
#-*- coding: utf-8 -*-
from abc import ABC, abstractmethod
class Device(ABC):
    @abstractmethod
    def __init__(self):
        self.interval = None
        self.ID = None
        self.description = None

    @abstractmethod
    def setInterval(self, interval):
        pass

    @abstractmethod
    def compress(self, ):
        pass

    @abstractmethod
    def analyze(self, data):
        pass

    def sendData(self, ):
        pass

    def pulseBroadCast(self, ):
        pass

    @abstractmethod
    def getData(self, ):
        pass

    def isReady(self, false):
        pass

    def createData(self, dataType):
        pass

    def setDescription(self, description):
        pass

