#!/usr/bin/python
#-*- coding: utf-8 -*-

# Interface
# import this to device to make the device support tensiometer sensor and behavior.
# all methods with "@abstractmethod" decorators are MUST be implementer into the sub class of this.
# please copy the comment "override from ***"  to the subclass to make the code more readable

from abc import ABC, abstractmethod

class tensiometer(ABC):

    m_humidity = None
    m_buttery = None

    Type = "Tensiometer"
    dataType = "text"

    # override from tensiometer
    @abstractmethod
    def getHumidity(self, ):
        pass

    # override from tensiometer
    @abstractmethod
    def needToClean(self, ):
        pass

    def getDataType(self):
        return "text"

    def printMyType(self):
        print("Device type: Tensiometer")

    @abstractmethod
    # override from tensiometer
    def getData(self):
        print("\ntensiometer:  Get Data:\n---------------")
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
    #override from tensiometer
    def getSettings(self):
        print("\ntensiomete: Get Settings:\n-------------------------")
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

    # override from tensiometer
    @abstractmethod
    def analyze(self):
        print("\ntensiometer: analyze:\n-----------------------")
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

    # override from tensiometer
    @abstractmethod
    def compareData(self):
        print("tensiometer: compare data\n-------")
        print("tensiometer compareData(): data has changed--> returns true\n-------") #todo: just for test in case its really true
        #todo: implement code for comparing old data from sensor to new data from sensor
        return False #todo return true only if data has changed- just for test. need to see if its really true

    # override from tensiometer
    @abstractmethod
    def dataReduction(self):
        print("tensiometer: Make Reduction to data:\n-------")
        #todo: implement code for the data reduction