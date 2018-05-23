#!/usr/bin/python
#-*- coding: utf-8 -*-

# Interface
# import this to device to make the device support tensiometer sensor and behavior.
# all methods with "@abstractmethod" decorators are MUST be implementer into the sub class of this.
# please copy the comment "override from ***"  to the subclass to make the code more readable
import datetime
from abc import ABC, abstractmethod

from pydub import AudioSegment


class microphone(ABC):


    Type = "Microphone"
    dataType = "audio"
    fileExtension = "wav"
    needReduction = "False"
    needCompression = "True"

    def getDataType(self):
        return "audio"

    def printMyType(self):
        print("Device type: Microphone")

    @abstractmethod
    # override from microphone
    def getData(self):
        print("microphone:  Get Data:")
        pass


    @abstractmethod
    #override from microphone
    def getSettings(self):
        print("microphone: Get Settings:")
        pass

    # override from microphone
    @abstractmethod
    def analyze(self):
        print("microphone: analyze:")
        pass

    # override from microphone
    @abstractmethod
    def compareData(self):
        print("microphone: compare data")
        print("microphone compareData(): data has changed--> returns true") #todo: just for test in case its really true
        #todo: implement code for comparing old data from sensor to new data from sensor
        return True #todo return true only if data has changed- just for test. need to see if its really true

    # override from microphone
    @abstractmethod
    def dataReduction(self, files):
        print("microphone: Make Reduction to data:")
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        song = AudioSegment.from_wav(files[0]).export("filesAfterReduce/convertedFile-" + date + ".mp3",format="mp3")  # convert wav to mp3
        print("microphone: Audio file converted to mp3 successfully:")