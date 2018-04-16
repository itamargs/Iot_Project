#!/usr/bin/python
#-*- coding: utf-8 -*-

# Interface
# import this to device to make the device support tensiometer sensor and behavior.

from abc import ABC, abstractmethod

class tensiometer(ABC):

    m_humidity = None
    m_buttery = None

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

    @abstractmethod
    def getData(self):
        print("\nGet Data:\n---------------")
        # 1. Alpha -> get text dummy file. Beta-> get real data from sensor and convert it to text file
        my_dict = {}
        file = open("tensiometer_output.txt", "r")
        for line in file:
            if ':' not in line:
                continue
            k = line.strip().split(':')[0]  # name
            v = line.strip().split(':')[1]  # value
            my_dict[k] = v

        for key, value in my_dict.items():
            print(key + ":", value)


    @abstractmethod
    def getSettings(self):
        print("\nGet Settings:\n----------------")
        my_dict = {}
        file = open("tensiometer_settings.txt", "r")
        for line in file:
            if ':' not in line:
                continue
            k = line.strip().split(':')[0]  # name
            v = line.strip().split(':')[1]  # value
            my_dict[k] = v

        for key, value in my_dict.items():
            print(key + ":", value)


    @abstractmethod
    def analyze(self):
        print("\nanalyze:\n-------")
        my_dict = {}
        file = open("tensiometer_output.txt", "r")
        for line in file:
          if ':' not in line:
            continue
          k = line.strip().split(':')[0]  # name
          v = line.strip().split(':')[1]  # value
          my_dict[k] = v

        m_humidity = my_dict.get('humidity', 'None')
        m_buttery = my_dict.get('buttery', 'None')

