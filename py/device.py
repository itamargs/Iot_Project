#!/usr/bin/python
# -*- coding: utf-8 -*-
# interface

import datetime
import glob
from abc import ABC, abstractmethod
import pickle  # saving object for other sessions
from time import sleep
import dill as pickle
import socket
import os
import time
import zlib



class device(ABC):

    def __init__(self, interval, ID, description):
        self.interval = interval
        self.ID = ID
        self.description = description
        self.dataType = self.dataType
        self.mode = "standBy"  #device state: standby= regular mode (waiting for something to happen)
        print("device: init device:", description)

    def save(self, path):
        with open(path, 'wb') as f:
            return pickle.dump(self, f)

    def load(self, path):
        with open(path, 'rb') as f:
            self.__dict__.update(pickle.load(f).__dict__)


    # override from device
    def setInterval(self, interval):  # interval for heart beat send
        pass

    #override from device
    def doesNeedAnalyzing(self):   # is the data need to be analyzed (example: if only 1 second past from last time there is no need)
        # print("device: check if need analyze")
        return True  # todo: just place holder, need to check if need analyze

    # override from device
    def deleteOutdatedData(self):  # delete data who isn't nececcery anymore for cleaning space in device memory
        print("device: deleteOutdatedData")
        pass


    def getReady(self):  # final initializaion of device
        print("device: Getting ready...")
        self.getData()  # get data from device (data depends on device type)
        self.getSettings()  # get settings from device (settings depends on device type)
        self.analyze()  # insert values from sensor uoutput into device data members
        pass

    def isTheDataHasChanged(self):  # boolean
        print("device: Check for change in data...")
        return self.compareData()  # compare the new data from the sensor to the data captured last time. (return true if data has changed)

    def getChange(self):  # get the change from the old data that captured in sensor to the new data captured
        print("device: get the change in data...")
        # todo: place holder. need to write the method
        pass

    def sendPulse(self):  # pulse heart beat to the server
        print("device: sending pulse")
        pass

    def isReady(self, false):  # is the device ready to send data amd etc?
        pass

    def createData(self, dataType):  # create the data file
        pass

    def setDescription(self, description):  # set a new (textual) description to the device
        pass

    def deleteOutDatedData(self):
        pass  # todo: place holder. need to write the method



    def printDetails(self):
        print("ID:", self.ID)
        print("Interval:", self.interval)
        print("Description:", self.description)
        print("Data Type:", self.dataType)

    # path to folder fo files to get
    def getDataFromInputFolder(self, path):
        # print("Searching for files in input directory...")
        files = glob.glob(path + "/*.*")  # create list of files in directory
        try:
            while not files:
                sleep(10)
                files = glob.glob(path + "/*.*")
            else:  # then list (actually the directory) isn't empty
                # print("File detected!") #todo Filedetected message is duplicate because its also says it in the standby mode.
                return (files)
        except KeyboardInterrupt:
            print("Exit Stand By mode")
            pass

    # 'files': what files[0] to compress. 'path': to file goes after compress
    def compress(self, files, path, deviceID, date):  #   compress data with some known compress method
        #compress the data
        print("device: compressing data")
        original_data = open(files[0], 'rb').read()
        compressed_data = zlib.compress(original_data, zlib.Z_BEST_COMPRESSION)

        # compress_ratio = (float(len(original_data)) - float(len(compressed_data))) / float(len(original_data))
        # print('Compressed: %d%%' % (100.0 * compress_ratio))

        #save the compressed data to file
        f = open(path + '/' + deviceID + '-' + date + '.zlib', 'wb')
        f.write(compressed_data)
        f.close()

    def sendData(self, path): # send data to Master
        print("device: sending data")

        dirs = os.listdir(path)

        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = "127.0.0.1"
            port = 5002
            try:
                sock.connect((host, port))
                break
            except:
                print("Falied to connect, auto try again after 10sec")
                time.sleep(10)
                continue

        total_size = 0

        print("CONECT TO MASTER")
        for files in dirs:
            filename = files
            size = len(filename)            #num of lines in files
            size = bin(size)[2:].zfill(16)  # encode file name to 16 bit, zfill for not losing the leading zero when converting to bin
            sock.sendall(size.encode('utf8'))  # encode so we could send it
            sock.sendall(filename.encode('utf8'))

            filename = os.path.join(path, filename) #gets the full file name
            filesize = os.path.getsize(filename)    #gets the real file size after reduce
            total_size += filesize
            filesize = bin(filesize)[2:].zfill(32)  # encode filesize as 32 bit binary
            sock.sendall(filesize.encode('utf8'))

            file_to_send = open(filename, 'rb')

            l = file_to_send.read()
            sock.sendall(l)
            file_to_send.close()

        conf =  sock.recv(4096)

        if (conf.decode('utf8') == str(total_size)):
            print("all files recvied successfully")

        sock.close()

        filelist = [f for f in os.listdir(path)]
        for f in filelist:
            os.remove(os.path.join(path, f))



    def noChange(self):
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = "127.0.0.1"
            port  = 5002
            try:
                sock.connect((host, port))
                break
            except:
                print("Falied to connect, auto try again after 10sec")
                time.sleep(10)
                continue

        print("no change")
        sock.sendall(("No Change").encode('utf8'))
        sock.close()

