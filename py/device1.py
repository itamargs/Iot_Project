# this is a device.
# import here the interface "device" to make it able to act as device who can work with the compressing protocol
#impot tensiometer to make this device be able to connect to a tensiometer sensor

import device
import tensiometer
import switch


class device1(device.device, tensiometer.tensiometer):

    # override from device
    def setInterval(self, interval):
        # interval for heart beat send
        pass

    # override from device
    def compress(self):
        #   generic compression method by the data type of the device
        pass

    #override from device
    def doesNeedAnalyzing(self):   # is the device need to be analyzed
        pass

    # override from tensiometer
    def analyze(self, data):
        # make data ready to read by the protocol
        pass

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
        super(device1, self).compareData()

    # override from tensiometer
    def dataReduction(self):
        super(device1, self).dataReduction()


# This code is generic. it works with all type of devices depends on the device type we imported


option = 'first start'  # todo: for test propoose only


for case in switch(option):
    if case('first start'):
        print("case: first start")
        myDevice = device1(10, 5645656656, "my IoT device")
        myDevice.getReady()
        # check if need start analyze data
        if myDevice.doesNeedAnalyzing() is True:
            myDevice.analyze()
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

    if case('new data'): #need to load the object created in the case of "first start"
        print("case: new data")
        if myDevice.doesNeedAnalyzing() is True:
            myDevice.analyze()
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

    if case('interval activation'):
        print("case: interval activation")
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




