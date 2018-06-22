# this is a device.
# import here the interface "device" to make it able to act as device who can work with the compressing protocol
#impot tensiometer to make this device be able to connect to a tensiometer sensor.


import tensiometer

import datetime
import device
from switch import switch #import class switch from file switch
import pickle #saving object for other sessions
import dill as pickle
from pydub import AudioSegment
import pydub
import os.path
import time
import glob
import shutil
import os
import ntpath
from pathlib import Path

class Device(device.device, tensiometer.tensiometer): #tensiometer is a placeholder

    # override from tensiometer
    def getHumidity(self, ):
        pass

    # override from tensiometer
    def needToClean(self, ):
        pass

    # override from tensiometer
    def dataReduction(self, files, path):
        super(Device, self).dataReduction(files, path)




# The code below is generic. it works with all type of devices depends on the device type we imported



option = None # :-)

while(True):
    if option == None:
        print("\nInsert case NUM:\n"
              " 1: first start\n"
              # " 2: new data (trigger received)\n"
              # " 3: interval activation (or ping from server)\n"
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
            print("\ncase: first start")
            myDevice = Device(1, "0022", "my Tesnsiometer IoT device") #(self, interval, id, description)create device instance to actually run in background and gather data
            myDevice_ = myDevice.save('saved') #saving the device values to another sessions
            myDevice.printDetails()
            print("--Sucess--")
            option = None
            break



        if case('new data'):  # need to load the object created in the case of "first start"
            print("case: new data")
            with open('saved', 'rb') as f:
                myDevice = pickle.load(f)
            if myDevice.doesNeedAnalyzing() is True:
                files = myDevice.getDataFromInputFolder("filesPool")  # get list of pointers to the files in the path provided folder
                original_file_name = Path(files[0]).stem
                filename123, original_file_extension = os.path.splitext(files[0])
                # todo: date won't change fast enogh if multiple files was forced copoid into input folder. can cause error in creating file  (won't be the case in production mode)
                date = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
                print("file name:" + original_file_name)
                # myDevice.analyze()
                # if myDevice.isTheDataHasChanged() is True:  # if there is a change
                # myDevice.getChange()  # data has been changed so get the new data
                # myDevice.compareData()
                # reducing or compressing the files depends on their sensor settings
                if myDevice.needReduction is True: # is the file need to go throw reduction process
                    result = myDevice.dataReduction(files[0], "filesUnderProcess") # make reduction + save result in this path
                    if result is False: # result is false when there is error in reduction
                        os.remove(files[0]) # remove the file that cause the error so can keep program flow
                        option = "standBy" # go back to standby mode
                        break
                    filename, file_extension = os.path.splitext(files[0])
                    if myDevice.save_original_file is True:
                        shutil.move(files[0],
                                    "filesBeenCared/" + myDevice.ID + "-" + date + file_extension)  #

                    try: # need to remove file from filesUnderProcess DIR. if we wanted to save original the file, the file wont be there so need to check that.
                        os.remove(files[0])
                    except FileNotFoundError:
                        pass

                    if myDevice.needCompression is False:
                        files = myDevice.getDataFromInputFolder("filesUnderProcess")
                        filename, file_extension = os.path.splitext(files[0])
                        shutil.move(files[0],
                                         "readyFiles/" + myDevice.ID + "-" + date + file_extension)  # rename and move file to new folder
                    if myDevice.needCompression is True:
                        files = myDevice.getDataFromInputFolder("filesUnderProcess")
                        myDevice.compress(files, "readyFiles", myDevice.ID, date)
                        os.remove(files[0])

                elif myDevice.needCompression is True:
                    files = myDevice.getDataFromInputFolder("filesPool")
                    myDevice.compress(files, "readyFiles", myDevice.ID, date) # compress file + save result in this path
                    if myDevice.save_original_file is True:
                        shutil.move(files[0],
                                    "filesBeenCared/" + myDevice.ID + "-" + date + original_file_extension)
                    try: # need to remove file from filePool DIR. if we wanted to save original file, the file wont be there so need to check that.
                        os.remove(files[0])
                    except FileNotFoundError:
                        pass


                # myDevice.deleteOutdatedData()
                # myDevice.sendPulse()
                myDevice.sendData("readyFiles")  #Send all files inside path to the server
                # waitForFileCreation()
            else:  # if there is NO change
                myDevice.deleteOutdatedData()
                # myDevice.sendPulse()
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
                # myDevice.sendData()
            else:  # if there is NO change
                myDevice.deleteOutdatedData()
                myDevice.sendPulse()
            option = None
            break



        if case('standBy'):
            print("\nWelcome to project Ultron.\nStand by, We R Waiting for new data\n.")
            while (True):
                print("Searching for files in input directory...") #todo: implements other trigers then new file
                filesExist = glob.glob("filesPool/*.*")  # create list of files in directory
                try:
                    while not filesExist:
                        myDevice.noChange()
                        time.sleep(4)
                        filesExist = glob.glob("filesPool/*.*")
                    else:  # then list (actually the directory) isn't empty
                        print("File detected!")
                        option = "new data"
                        break
                except KeyboardInterrupt:
                    print("Exit Stand By mode")
                    pass


        if case(): # default, could also just omit condition or 'if True'
            pass
            # No need to break here, it'll stop anyway
