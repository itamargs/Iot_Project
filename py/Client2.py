import glob
from abc import ABC, abstractmethod
import pickle  # saving object for other sessions
from time import sleep
import dill as pickle
import socket
import os
import time
import zlib


def sendData(self, path):
    print("device: sending data")

    dirs = os.listdir(path)

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"
        port  = 5002
        try:
            sock.connect((host, port))
            break
        except:
            print("Falied to connect, auto try again after 5sec")
            time.sleep(5)
            continue


    for files in dirs:
        filename = files
        size = len(filename)
        size = bin(size)[2:].zfill(16) #encode file name to 16 bit
        sock.sendall(size.encode('utf8'))
        sock.sendall(filename.encode('utf8'))

        filename = os.path.join(path,filename)
        filesize = os.path.getsize(filename)
        filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
        sock.sendall(filesize.encode('utf8'))

        file_to_send = open(filename, 'rb')

        l = file_to_send.read()
        sock.sendall(l)
        file_to_send.close()

    sock.close()

    filelist = [ f for f in os.listdir(path)]
    for f in filelist:
        os.remove(os.path.join(path, f))


