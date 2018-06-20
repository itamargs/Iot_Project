import os
import socket
from datetime import datetime
from threading import Thread
import time
import firebase_admin
import pyrebase
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

thread_check_for_internet_exist = False
sombodySendToCloud = False


def init_fireBase():
    global cred
    global config
    global firebase
    global db
    global bucket
    global py_storage
    global firebaseIsON


    # ------------------------------------------  Init FireStore ------------------------------------------------------
    # - we use the variable name'pystorage' instead of the variable name 'storage' for pyrebase use for not colliding with the native firebase which we use it for firestore
    # - note that we will use pyrebase only for firebase 'Storage' and not
    #   for the real time databae as we use FireStore instead- Cause FireStore already have a python native functions
    # - init fireStore cloud with credentials and Etc.

    cred = credentials.Certificate('/home/itamar/iotproject-dd956-4555a8fff398.json')
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
    global thread_check_for_internet_exist
    global sombodySendToCloud
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
        print('File received successfully from Device')

        sendFileToCloud('', serverID, filename)

#starting server with the connection defantion

def fileSyncHandlerThread(serverID):
    while True:
        if not have_internet():
                while have_internet() is False:
                    print("no internet - will check again in 5 seconds")
                    time.sleep(5)
                print("internet connection back on :) -> sync files")
                while sombodySendToCloud == True:
                    time.sleep(2)
                files_db('', serverID)
        time.sleep(5)
        print("handle thread: All OK")


def startserver():


    serverID = "0001"

    os.chdir('Recvied')
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 5002;
    serversock.bind((host,port));
    filename = ""
    serversock.listen(1);
    print ("Waiting for a connection.....")

    try:
        thread = Thread(target = fileSyncHandlerThread, args=(serverID,))
        thread.start()
    except:
        print("Error trying to create Thread")

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
def sendFileToCloud(self, serverID, fileName):
    global sombodySendToCloud
    sombodySendToCloud = True
    fileName = fileName.decode('utf-8')

    internetOn = have_internet() # for checking internet connection only once
    server_id = serverID
    dirs = os.listdir()
    for files in dirs:  # scanning the whole folder given- 'files' is a single file inside a folder
        if files == fileName:
            device_id = fileName.rsplit('-')[0]
            temp_date = fileName.rsplit('-')[1]                                                        #split the time so it would be readable
            date =str( datetime(int(temp_date[4:]), int(temp_date[2:4]), int(temp_date[:2])))       #contain the relvant date but in full format
            temp_time = fileName.rsplit('-')[2].rsplit('.')[0]
            mtime = str(temp_time[0:2]) + ':' + str(temp_time[2:4]) + ':' + temp_time[4:]

            print("current file name:" + fileName)


            # now saving data in cloud
            if not firebaseIsON and internetOn:
                init_fireBase()
            if internetOn and firebaseIsON:
                print("OKKKKKKKK Updating FireBase")
                destinationFileName = server_id + "-" + fileName
                blob = bucket.blob(destinationFileName)  # destination file name in Google Storage
                blob.upload_from_filename(fileName)  # file location on local device
                # fileUrl = py_storage.child(fileName).get_url(None) # get url of file from Google Storage
                fileUrl = 'https://storage.cloud.google.com/' + bucket.name +'/' + destinationFileName
                print(fileUrl)

                data = {
                    u'file_name': fileUrl,
                    u'date': date[0:10],
                    u'time': mtime,
                }
                db.collection('Master ID:' + server_id).document('Device ID:' + device_id).collection('fileName').document(fileName).set(data)
                try:
                    os.remove(fileName)
                    print("file: " + fileName + ' removed sucecfuly')
                except FileNotFoundError:
                    print("ERROR: Can't erase synced file (Probably user try to copy multiple file into input dir)")

            else:
                print("try to send data to cloud but no internet")
    sombodySendToCloud = False

#creating Server DB
def files_db(self, serverID):
    internetOn = have_internet() # for checking internet connection only once

    server_id = serverID
    dirs = os.listdir()



    for files in dirs:  #scanning the whole folder given- 'files' is a single file inside a folder

        device_id = files.rsplit('-')[0]
        temp_date = files.rsplit('-')[1]                                                        #split the time so it would be readable
        date =str( datetime(int(temp_date[4:]), int(temp_date[2:4]), int(temp_date[:2])))       #contain the relvant date but in full format
        temp_time = files.rsplit('-')[2].rsplit('.')[0]
        mtime = str(temp_time[0:2]) + ':' + str(temp_time[2:4]) + ':' + temp_time[4:]

        print("current file name:" + files)


        # now saving data in cloud
        if not firebaseIsON and internetOn:
            init_fireBase()
        if internetOn and firebaseIsON:
            print("OKKKKKKKK Updating FireBase")
            destinationFileName = server_id + "-" + files
            blob = bucket.blob(destinationFileName)  # destination file name in Google Storage
            blob.upload_from_filename(files)  # file location on local device
            # fileUrl = py_storage.child(files).get_url(None) # get url of file from Google Storage
            fileUrl = 'https://storage.cloud.google.com/' + bucket.name +'/' + destinationFileName
            print(fileUrl)

            data = {
                u'file_name': fileUrl,
                u'date': date[0:10],
                u'time': mtime,
            }
            db.collection('Master ID:' + server_id).document('Device ID:' + device_id).collection('Files').document(files).set(data)

            print("removing file after the backup :" + files)
            os.remove(files)

        else:
            print("try to send data to cloud but no internet")



startserver()
