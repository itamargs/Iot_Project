import device
import tensiometer


class device1(device.device, tensiometer.tensiometer):


    def setInterval(self, interval):
        # interval for heart beat send
        pass

    def compress():
      #   generic compression method by the data type of the device
      pass

    def analyze(self, data):
     # make data ready to read by the protocol
     pass

    def getData(self):  #get the data from sensor according to his type
     # get data from sensor
        super(device1,self).getData()

    def getSettings(self):  #get settings from file
     # get data from sensor
        super(device1,self).getSettings()

    def analyze(self):  #get settings from file
        # analyze data in sensor, isert values to class values
        super(device1,self).analyze()

    def getHumidity(self, ):
     # get humidity from tensiometer
     pass


    def needToClean(self, ):
     # if need to clean tensiometer
     pass






myDevice = device1(10, 1234567, "my first device")
myDevice.getReady()


# myDevice.printMyType()
# myDevice.printDetails()
# print(myDevice.getDataType())


