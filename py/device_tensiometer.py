# this is a device.
# import here the interface "device" to make it able to act as device who can work with the compressing protocol
#impot tensiometer to make this device be able to connect to a tensiometer sensor


import device
import tensiometer
from switch import switch #import class switch from file switch
import pickle #saving object for other sessions
import dill as pickle

class device1(device.device, tensiometer.tensiometer): #tensionmeter is a placeholder


    # override from device
    def setInterval(self, interval):
        # interval for heart beat send
        pass


    #override from device
    def deleteOutdatedData(self):   # delete data who isn't nececcery anymore for cleaning space in device memory
        super(device1, self).deleteOutdatedData()
        pass

    # override from tensiometer
    def analyze(self, data):
        # make data ready to read by the protocol
        super(device1, self).analyze()

    # override from tensiometer
    def getData(self):  #get the data from sensor according to his type
        # get data from sensor
        super(device1,self).getData()

    # override from tensiometer
    def getSettings(self):  #get settings from file
        # get data from sensor
        super(device1,self).getSettings()

    # override from tensiometer
    def analyze(self):  #get settings from file
        # analyze data in sensor, insert values to class values
        super(device1,self).analyze()

    # override from tensiometer
    def getHumidity(self, ):
        # get humidity from tensiometer
        pass

    # override from tensiometer
    def needToClean(self, ):
        # if need to clean tensiometer
        pass

    # override from tensiometer
    def compareData(self):
        return super(device1, self).compareData() #return tu super cause result should RETURN "False" or "True"

    # override from tensiometer
    def dataReduction(self):
        super(device1, self).dataReduction()



# This code is generic. it works with all type of devices depends on the device type we imported

#todo: remove this testing section
#----------------------  TESTING ONLY ----------------------------
# option = 'first start'  # todo: for test propoose only
# option = 'first start'  # todo: for test propoose only

print("Insert case NUM:\n"
      " 1: first start\n"
      " 2: new data (triger recived)\n"
      " 3: interval activation\n")
option = input("insert NUM: ")
if option == "1":
    option = "first start"
if option == "2":
    option = "new data"
if option == "3":
    option = "interval activation"
#----------------------  END OF TESTING ONLY ----------------------------


for case in switch(option):
    if case('first start'):
        print("case: first start")
        myDevice = device1(10, 5645656656, "my IoT device") #(self, interval, id, description)create device instance to actually run in background and gather data
        myDevice_ = myDevice.save('saved') #saving the device values to another sessions

        # myDevice.getReady()
        # check if need start analyze data
        if myDevice.doesNeedAnalyzing() is True:
                myDevice.analyze()
                if myDevice.isTheDataHasChanged() is True:  # if there is a change #todo: why its not return true???
                    myDevice.getChange()  # data has been changed so get the new data
                    myDevice.dataReduction()
                    myDevice.compress()
                    myDevice.deleteOutdatedData()
                    myDevice.sendPulse()
                    myDevice.sendData()
                else:  # if there is NO change
                    myDevice.deleteOutdatedData()
                    myDevice.sendPulse()
        break

#todo: recheck if need to remove "#" from part of the methods
    if case('new data'): #need to load the object created in the case of "first start"
        print("case: new data")
        with open('saved', 'rb') as f:
            myDevice = pickle.load(f)
        if myDevice.doesNeedAnalyzing() is True:
            myDevice.analyze()
            if myDevice.isTheDataHasChanged() is True:  # if there is a change
                # myDevice.getChange()  # data has been changed so get the new data
                # myDevice.compareData()
                myDevice.dataReduction()
                myDevice.compress()
                myDevice.deleteOutdatedData()
                myDevice.sendPulse()
                myDevice.sendData()
        else:  # if there is NO change
            myDevice.deleteOutdatedData()
            myDevice.sendPulse()
        break

    if case('interval activation'):
        print("case: Interval activation")
        with open('saved', 'rb') as f:
            myDevice = pickle.load(f)
        # todo:pulseCheck()
        if myDevice.isTheDataHasChanged() is True:  # if there is a change
            myDevice.getChange()  # data has been changed so get the new data
            myDevice.compareData()
            myDevice.dataReduction()
            myDevice.compress()
            myDevice.deleteOutdatedData()
            myDevice.sendPulse()
            myDevice.sendData()
        else:  # if there is NO change
           myDevice.deleteOutdatedData()
           myDevice.sendPulse()
        break



    # if case('two'):
    #     print 2
    #     break

    if case(): # default, could also just omit condition or 'if True'
        print("something else!")
        # No need to break here, it'll stop anyway




