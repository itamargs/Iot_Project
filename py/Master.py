import socket
import os
import sys
from threading import Thread
import hashlib
from pprint import pprint as pp
from datetime import datetime
import pprint
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
try:
    import httplib
except:
    import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


cred = None
config = None
firebase = None
db = None
bucket = None
py_storage = None
firebaseIsON = False


def init_fireBase():
    global cred
    global config
    global firebase
    global db
    global bucket
    global py_storage
    global firebaseIsON
    # ------------------------------------------  Init FireStore ------------------------------------------------------
    # - we use 'pystorage' instead of 'storage' for pyrebase use for not colliding with the native firebase which we use it for firestore
    # - note that we will use pyrebase only for firebase 'Storage' and not
    # - for the real time databae as we use Dire Store
    # - instead and fire store already have a python native functions
    # - init fireStore cloud with credentials and things -

    cred = credentials.Certificate('/home/itamar/iotproject-dd956-4555a8fff398.json')
    # - firebase_admin.initialize_app(cred)
    # - init FB app with credentials AND storage bucket (bucket is the thing that stores the data inside FB)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'iotproject-dd956.appspot.com'
    })
    # config values for pyrebase
    config = {
        "apiKey": "AIzaSyChiOWAbg8Th2woLuAXfpqJwUc2ajFvlkU",
        "authDomain": "iotproject-dd956.firebaseapp.com",
        "databaseURL": "https://iotproject-dd956.firebaseio.com",
        "storageBucket": "iotproject-dd956.appspot.com",
        "serviceAccount": "/home/itamar/iotproject-dd956-4555a8fff398.json"
    }
    firebase = pyrebase.initialize_app(config)
    db = firestore.client()
    # 'bucket' is an object defined in the google-cloud-storage Python library.
    # See https://google-cloud-python.readthedocs.io/en/latest/storage/buckets.html
    # for more details.
    bucket = storage.bucket()
    py_storage = firebase.storage()  # init firebase storage to work with pyrebase
    print('Fire Base Bucket name: "{}" .\n'.format(bucket.name))
    firebaseIsON = True
    # ---------------------- End of init FireBase -----------------------------------------------------------------------


if have_internet():
    init_fireBase()
else:
    print("try to init firebase but no internet access")


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


    serverID = "2"
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
    internetOn = have_internet() # for checking internet connection only once

    server_id = serverID

    files_dict ={}
    dirs = os.listdir()



    for files in dirs:  #scanning the whole folder given- 'files' is a single file inside a folder
        if files == 'db.txt':
            continue
        if files.rsplit('-')[0] not in files_dict:                                               #check if we still did not recvied file from that ID
            files_dict[files.rsplit('-')[0]] = {}
        device_id = files.rsplit('-')[0]
        temp_date = files.rsplit('-')[1]                                                        #split the time so it would be readable
        date =str( datetime(int(temp_date[4:]), int(temp_date[2:4]), int(temp_date[:2])))       #contain the relvant date but in full format
        temp_time = files.rsplit('-')[2].rsplit('.')[0]
        time = str(temp_time[0:2]) + ':' + str(temp_time[2:4]) + ':' + temp_time[4:]

        files_dict[files.rsplit('-')[0]][files] = {'date: ': date[0:10] , 'time: ': time, 'synced': False}

        print("current file name:" + files)


        # now saving data in cloud
        if not firebaseIsON and internetOn:
            init_fireBase()
        if internetOn and firebaseIsON:
            print("OKKKKKKKK Updating FireBase")
            blob = bucket.blob(server_id + "-" + files)  # destination file name in Google Storage
            blob.upload_from_filename(files)  # file location on local device
            fileUrl = py_storage.child(files).get_url(None) # get url of file from Google Storage

            data = {
                u'file_name': fileUrl,  # to fix e
                u'date': date[0:10],
                u'time': time,
            }
            db.collection(server_id).document(device_id).set(data)


            #todo all the files data on DB writen again every time it makes the synced value be overriden.
            # tag current file as synced to the cloud
            fileDict = files_dict[files.rsplit('-')[0]][files]
            fileDict.update(synced = True)
            files_dict[files.rsplit('-')[0]][files] = fileDict

        else:
            print("try to send data to cloud but no internet")



    with open('db.txt', 'w') as file:
        file.write(pprint.pformat(files_dict))


    pp(files_dict)



startserver()
