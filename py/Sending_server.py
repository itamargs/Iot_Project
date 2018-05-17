# import socket
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# address =('localhost', 5002)
#
# sock.bind(address)
#
# while True:
#     data, addr = sock.recvfrom(1024)
#     print(data)
#     print(addr)

import socket

host = ""
port = 5002

sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

while True:
    conn, addr = sock.accept()

    f = open("new_file.txt", 'wb')
    while True:
        data = conn.recv(1024)
        if not data:
            break
        f.write(data)
    f.close()
