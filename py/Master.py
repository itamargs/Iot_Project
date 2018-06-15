import socket
import os
from threading import Thread
import hashlib
from pprint import pprint as pp
from datetime import datetime
import pprint

#handle the clinets connection
def client_thread(clientsocket, ip, port,serverID , MAX_BUFFER = 4096):       # MAX_BUFFER_SIZE is how big the message can be
    while True:

        #recv file size from client
        size = clientsocket.recv(16)

        if size.decode('utf8') == "No Change":
            print("No Change detected")
            break


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
        files_db('', serverID)



#starting server with the connection defantion
def startserver():

    serverID = "1"
    os.chdir('Recvied')
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 5002;
    serversock.bind((host,port));
    filename = ""
    serversock.listen(1);
    print ("Waiting for a connection.....")

    #Infinte loop - so the server wont reset after each connetion
    while True:

        clientsocket,addr = serversock.accept()
        ip, port = str(addr[0]), str(addr[1])
        print("Got a connection from %s"+ ip + ":" + port)

        try:
           Thread(target = client_thread , args=(clientsocket, ip, port, serverID)).start()

        except:
            print("Error trying to create Thread")

    serversock.connect(ip, port)
    serversock.sendall("Recvied".encode('utf8'))
    serversock.close()





#creating Server DB
def files_db(self, serverID):
    server_id = serverID

    files_dict ={}
    dirs = os.listdir()

    for files in dirs:                                                                          #scanning the whole flder given
        if files == 'db.txt':
            continue
        if files.rsplit('-')[0] not in files_dict:                                               #check if we still did not recvied file from that ID
            files_dict[files.rsplit('-')[0]] = {}
        device_id = files.rsplit('-')[0]
        temp_date = files.rsplit('-')[1]                                                        #split the time so it would be readable
        date =str( datetime(int(temp_date[4:]), int(temp_date[2:4]), int(temp_date[:2])))       #contain the relvant date but in full format
        temp_time = files.rsplit('-')[2].rsplit('.')[0]
        time = str(temp_time[0:2]) + ':' + str(temp_time[2:4]) + ':' + temp_time[4:]

        files_dict[files.rsplit('-')[0]][files] = {'date: ': date[0:10] , 'time: ': time}

    with open('db.txt', 'w') as file:
        file.write(pprint.pformat(files_dict))


    pp(files_dict)



startserver()
