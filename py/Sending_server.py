import socket

host = ""
port = 5002

sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

while True:
    conn, addr = sock.accept()

    f = open("new_file.wav", 'wb')
    while True:
        data = conn.recv(1024)
        if not data:
            sock.send("OK")
            break
        f.write(data)
f.close()
