# The Master is controlling the "Device". Master send the devices data to the cloud

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

    cred = credentials.Certificate('iotproject-dd956-firebase-adminsdk-usn8m-50b069f476.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'iotproject-dd956.appspot.com'
    })
    # config values for pyrebase
    config = {
        "apiKey": "AIzaSyChiOWAbg8Th2woLuAXfpqJwUc2ajFvlkU",
        "authDomain": "iotproject-dd956.firebaseapp.com",
        "databaseURL": "https://iotproject-dd956.firebaseio.com",
        "storageBucket": "iotproject-dd956.appspot.com",
        "serviceAccount": "iotproject-dd956-firebase-adminsdk-usn8m-50b069f476.json"
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

        total_size = 0
        #recv file size from client
        size = clientsocket.recv(16)

        if size.decode('utf8') == "No Change":          #check if there is no change detected by client and print it
            print("No Change detected")
            break


        if not size:                                    #if client done sending
            break

        size = int(size, 2)
        filename = clientsocket.recv(size)              #gets the filename from client
        filesize = clientsocket.recv(32)                #gets the file size from cleint
        filesize = int(filesize, 2)
        file_to_write = open(filename, 'wb')            #creating the received file on server side with the original name

        chunksize = 4096
        while filesize > 0:                             #when filesize = 0, we received the entire file
            if filesize < chunksize:                    #if server get large file
                chunksize = filesize
            data = clientsocket.recv(chunksize)
            file_to_write.write(data)
            total_size += filesize
            filesize -= len(data)                        #subtrack what we received from the actual size

        file_to_write.close()
        clientsocket.sendall(((str(total_size)).encode(('utf8'))))
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
        print("File cloud sync: OK")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
	# doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def startserver():


    serverID = "0001"

    os.chdir('Recvied')
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = get_ip()
    port = 5000;
    print('Listen on: ' + host + ':' + str(port))
    serversock.bind((host,port));
    filename = ""
    serversock.listen(10);
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
        print("\nGot a connection from "+ ip + ":" + port)

        try:
           Thread(target = client_thread , args=(clientsocket, ip, port, serverID)).start()

        except:
            print("Error trying to create Thread")



#sync recived file to cloud
def sendFileToCloud(self, serverID, fileName):
    global sombodySendToCloud
    sombodySendToCloud = True
    fileName = fileName.decode('utf-8')

    internetOn = have_internet() # for checking internet connection only once
    server_id = serverID
    dirs = os.listdir()
    for files in dirs:  # scanning the whole folder given- 'files' is a single file inside a folder
        if files == fileName:
            device_id = fileName.rsplit('-')[0] # export id
            temp_date = fileName.rsplit('-')[1]   # export date                                                     #split the time so it would be readable
            date =str( datetime(int(temp_date[4:]), int(temp_date[2:4]), int(temp_date[:2])))       #contain the relvant date but in full format
            # temp_time = fileName.rsplit('-')[2].rsplit('.')[0] # export time
            temp_time = fileName.rsplit('-')[2]  # export time
            mtime = str(temp_time[0:2]) + ':' + str(temp_time[2:4]) + ':' + temp_time[4:]
            fileExtension = fileName.rsplit('-')[3] # export file extension
            description = fileName.rsplit('-')[4] # export description

            print("File name:" + fileName)


            # now saving data in cloud
            if not firebaseIsON and internetOn:
                init_fireBase()
            if internetOn and firebaseIsON:
                print("OK, OK, OK, Updating FireBase")

                destinationFileName = server_id + "-" + fileName.rsplit('.')[0] + fileExtension
                blob = bucket.blob(destinationFileName)  # destination file name in Google Storage
                blob.upload_from_filename(fileName)  # file location on local device

                fileUrl = 'https://storage.cloud.google.com/' + bucket.name +'/' + destinationFileName # get url of file from Google Storage
                print(fileUrl)

                data = {
                    u'file_name': fileUrl,
                    u'date': date[0:10],
                    u'time': mtime,
                    u'description': description,
                }
                db.collection('Master ID:' + server_id).document('Device ID:' + device_id).collection('Files').document(fileName.rsplit(fileExtension)[0] + fileExtension).set(data)
                try:
                    os.remove(fileName)
                    print("file removed sucecfuly from master")
                except FileNotFoundError:
                    print("ERROR: Can't erase synced file (Probably user try to copy multiple file into input dir)")

            else:
                print("try to send data to cloud but no internet")
    sombodySendToCloud = False

#Sync files to cloud after getting back online to internet
def files_db(self, serverID):
    internetOn = have_internet() # for checking internet connection only once

    server_id = serverID
    dirs = os.listdir()



    for files in dirs:  #scanning the whole folder given- 'files' is a single file inside a folder

        device_id = files.rsplit('-')[0]  # export id
        temp_date = files.rsplit('-')[
            1]  # export date                                                     #split the time so it would be readable
        date = str(datetime(int(temp_date[4:]), int(temp_date[2:4]),
                            int(temp_date[:2])))  # contain the relvant date but in full format
        # temp_time = files.rsplit('-')[2].rsplit('.')[0] # export time
        temp_time = files.rsplit('-')[2]  # export time
        mtime = str(temp_time[0:2]) + ':' + str(temp_time[2:4]) + ':' + temp_time[4:]
        fileExtension = files.rsplit('-')[3]  # export file extension
        description = files.rsplit('-')[4]  # export description

        print("\nFile name:" + files)


        # now saving data in cloud
        if not firebaseIsON and internetOn:
            init_fireBase()
        if internetOn and firebaseIsON:
            print("OK, OK, OK Updating FireBase")
            destinationFileName = server_id + "-" + files.rsplit('.')[0] + fileExtension
            blob = bucket.blob(destinationFileName)  # destination file name in Google Storage
            blob.upload_from_filename(files)  # file location on local device
            # fileUrl = py_storage.child(files).get_url(None) # get url of file from Google Storage
            fileUrl = 'https://storage.cloud.google.com/' + bucket.name +'/' + destinationFileName
            print(fileUrl)

            data = {
                u'file_name': fileUrl,
                u'date': date[0:10],
                u'time': mtime,
                u'description': description,
            }
            db.collection('Master ID:' + server_id).document('Device ID:' + device_id).collection('Files').document(files.rsplit(fileExtension)[0] + fileExtension).set(data)
            try:
                os.remove(files)
                print("file removed sucecfuly from master")
            except FileNotFoundError:
                print("ERROR: Can't erase synced file (Probably user try to copy multiple file into input dir)")

        else:
            print("try to send data to cloud but no internet")



startserver()
