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

        filesExist = glob.glob("SendFiles/*.*")

        while True:
            if not filesExist:
                noChange('')
                time.sleep(4)
                filesExist = glob.glob("SendFiles/*.*")
            else:
                break


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


sendData('', 'SendFiles')
