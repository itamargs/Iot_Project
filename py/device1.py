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

    def getData(self):
     # get data from sensor
     pass


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


