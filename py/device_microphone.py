# this is a device.
# import here the interface "device" to make it able to act as device who can work with the compressing protocol
#impot tensiometer to make this device be able to connect to a tensiometer sensor
import datetime

import device
import microphone
from switch import switch #import class switch from file switch
import pickle #saving object for other sessions
import dill as pickle
from pydub import AudioSegment
import pydub
import os.path
import time
import glob
import shutil

class Device(device.device, microphone.microphone): #microphone is a placeholder


    # override from device
    def setInterval(self, interval):
        # interval for heart beat send
        pass


    #override from device
    def deleteOutdatedData(self):   # delete data who isn't nececcery anymore for cleaning space in device memory
        super(Device, self).deleteOutdatedData()
        pass

    # override from microphone
    def analyze(self, data):
        # make data ready to read by the protocol
        super(Device, self).analyze()

    # override from microphone
    def getData(self):  #get the data from sensor according to his type
        # get data from sensor
        super(Device, self).getData()

    # override from microphone
    def getSettings(self):  #get settings from file
        # get data from sensor
        super(Device, self).getSettings()

    # override from microphone
    def analyze(self):  #get settings from file
        # analyze data in sensor, insert values to class values
        super(Device, self).analyze()

    # override from microphone
    def compareData(self):
        return super(Device, self).compareData() #return tu super cause result should RETURN "False" or "True"

    # override from microphone
    def dataReduction(self, files):
        super(Device, self).dataReduction(files)




# This code is generic. it works with all type of devices depends on the device type we imported

#todo: remove this testing section
#----------------------  TESTING ONLY ----------------------------
# option = 'first start'  # todo: for test propoose only
# option = 'first start'  # todo: for test propoose only



#----------------------  END OF TESTING ONLY ----------------------------



option = None # :)

while(True):
    if option == None:
        print("\nInsert case NUM:\n"
              " 1: first start\n"
              " 2: new data (trigger received)\n"
              " 3: interval activation (or ping from server)\n"
              " 4: Stand By Mode")
        option = input("insert NUM: ")
        if option == "1":
            option = "first start"
        if option == "2":
            option = "new data"
        if option == "3":
            option = "interval activation"
        if option == "4":
            option = "standBy"

    for case in switch(option):

        if case('first start'):
            print("case: first start")
            myDevice = Device(10, 5645656656, "my  Microphone IoT device") #(self, interval, id, description)create device instance to actually run in background and gather data
            myDevice_ = myDevice.save('saved') #saving the device values to another sessions

            # myDevice.getReady()
            # check if need start analyze data
            if myDevice.doesNeedAnalyzing() is True:
                myDevice.analyze()
                if myDevice.isTheDataHasChanged() is True:  # if there is a change
                    # myDevice.getChange()  # data has been changed so get the new data
                    # myDevice.dataReduction()
                    # myDevice.compress()
                    # myDevice.deleteOutdatedData()
                    myDevice.sendPulse()
                    # myDevice.sendData()
                else:  # if there is NO change
                    # myDevice.deleteOutdatedData()
                    myDevice.sendPulse()
            option = None
            break

        #todo: recheck if need to remove "#" from part of the methods
        if case('new data'): #need to load the object created in the case of "first start"
            print("case: new data")
            with open('saved', 'rb') as f:
                myDevice = pickle.load(f)
            if myDevice.doesNeedAnalyzing() is True:
                files = myDevice.getDataFromInputFolder() #get pointer to the files in the input folder
                # myDevice.analyze()
                # if myDevice.isTheDataHasChanged() is True:  # if there is a change
                # myDevice.getChange()  # data has been changed so get the new data
                # myDevice.compareData()
                myDevice.dataReduction(files)
                date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                shutil.move(files[0],"filesAlreadyReduced/original-" + date + "." + myDevice.fileExtension)  # rename and move file to new folder with the device supported file extension
                myDevice.compress()
                # myDevice.deleteOutdatedData()
                myDevice.sendPulse()
                myDevice.sendData()
                # waitForFileCreation()
            else:  # if there is NO change
                myDevice.deleteOutdatedData()
                myDevice.sendPulse()
            option = "standBy"
            break

        if case('interval activation'):
            print("case: Interval activation")
            with open('saved', 'rb') as f:
                myDevice = pickle.load(f)
            # todo:pulseCheck()
            if myDevice.isTheDataHasChanged() is True:  # if there is a change
                # myDevice.getChange()  # data has been changed so get the new data
                # myDevice.compareData()
                # myDevice.dataReduction()
                # myDevice.compress()
                # myDevice.deleteOutdatedData()
                myDevice.sendPulse()
                myDevice.sendData()
            else:  # if there is NO change
                myDevice.deleteOutdatedData()
                myDevice.sendPulse()
            option = None
            break



        if case('standBy'):
            print("\nWelcome to project Ultron.\nStand by, We R Waiting for a trigger\n.")
            while (True):
                print("Searching for files in input directory...") #todo: implements other trigers then new file
                filesExist = glob.glob("filesToReduce/*.*")  # create list of files in directory
                try:
                    while not filesExist:
                        time.sleep(2)
                        filesExist = glob.glob("filesToReduce/*.*")
                    else:  # then list (actually the directory) isn't empty
                        print("File detected!")
                        option = "new data"
                        break
                except KeyboardInterrupt:
                    print("Exit Stand By mode")
                    pass


        if case(): # default, could also just omit condition or 'if True'
            print("something else!")
            # No need to break here, it'll stop anyway




