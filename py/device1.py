# this is a device.
# import here the interface "device" to make it able to act as device who can work with the compressing protocol
#impot tensiometer to make this device be able to connect to a tensiometer sensor

import device
import tensiometer


class device1(device.device, tensiometer.tensiometer):

    # override from device
    def setInterval(self, interval):
        # interval for heart beat send
        pass

    # override from device
    def compress():
      #   generic compression method by the data type of the device
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
        # analyze data in sensor, isert values to class values
        super(device1,self).analyze()

    # override from tensiometer
    def getHumidity(self, ):
     # get humidity from tensiometer
     pass

    # override from tensiometer
    def needToClean(self, ):
     # if need to clean tensiometer
     pass






myDevice = device1(10, 5645656656, "my IoT device")
myDevice.getReady()



