import socket
import os
import threading
import hashlib


def startserver():
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "127.0.0.1"
    port = 5002;
    serversock.bind((host,port));
    filename = ""
    serversock.listen(10);
    print ("Waiting for a connection.....")

    clientsocket,addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    while True:
        size = clientsocket.recv(16)                #recv file size from client
        if not size:
            break
        size = int(size, 2)
        filename = clientsocket.recv(size)
        filesize = clientsocket.recv(32)
        filesize = int(filesize, 2)
        file_to_write = open(filename, 'wb')            #creating the recived file on server side

        chunksize = 4096
        while filesize > 0:
            if filesize < chunksize:
                chunksize = filesize
            data = clientsocket.recv(chunksize)
            file_to_write.write(data)
            filesize -= len(data)

        file_to_write.close()
        print('File received successfully')

    serversock.close()


startserver()









