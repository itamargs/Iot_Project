4#!/usr/bin/python
#-*- coding: utf-8 -*-

# blueprint for sensor behavior
# Interface for microphone devices for using by the "Device" class

# copy part of this code (As it says on the "How to use" file) this to device to make the device support this sensor and behavior.
# all methods with "@abstractmethod" decorators are MUST be implementer into the sub class of this.
# please copy the comment "override from ***"  to the subclass to make the code more readable

import datetime
from abc import ABC, abstractmethod
from pydub import AudioSegment


class microphone(ABC):

    ##### modify here settings for the device #####
    Type = "Microphone"
    dataType = "audio"
    fileExtension = "wav"
    needReduction = True
    needCompression = True
    save_original_file = False
    INTERVAL = 1  # interval for device update in seconds
    MASTER_IP = "10.0.2.15"  # set here the ip of the master device
    DEVICE_DESCRIPTION = "My microphone device"  # give informative description to device
    DEVICE_ID = 1234 # give unique id for each device
    ###############      /SETINGS       ################

    # override from microphone
    @abstractmethod
    def analyze(self):
        print("microphone: analyze:")
        pass

    @abstractmethod
    # override from microphone
    def getData(self):
        print("microphone:  Get Data:")
        pass


    @abstractmethod
    #override from microphone
    def getSettings(self, deviceSettings):
        print("microphone: Get Settings:")
        deviceSettings = {"INTERVAL": "", "MASTER_IP": "", "DEVICE_DESCRIPTION": "", "DEVICE_ID": ""}
        return deviceSettings


    # override from microphone
    @abstractmethod
    def compareData(self):
        print("microphone: compare data")
        print("microphone compareData(): data has changed--> returns true") #todo: just for test in case its really true
        #todo: implement code for comparing old data from sensor to new data from sensor
        return True #todo return true only if data has changed- just for test. need to see if its really true

    # override from microphone
    @abstractmethod
    def dataReduction(self, file, path):
        print("microphone: Make Reduction to data:")
        date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        try:
            song = AudioSegment.from_wav(file).export(path + "/convertedFile-" + date + ".mp3",format="mp3")  # convert wav to mp3
        except:
            print("ERROR: Bad format. Please use .WAV for this device")
            return False

        print("microphone: Audio file converted to mp3 successfully:")
