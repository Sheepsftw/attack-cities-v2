import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = 'localhost'
port = 8080
sock.bind((host, port))
print('Server started')

while True:
    data, addr = sock.recvfrom(1024)
    data = data.decode('utf-8')
    print("Message from: " + str(addr))
    print("From connected user: " + data)
    data = data.upper()
    print("Sending: " + data)
    sock.sendto(data.encode('utf-8'), addr)

c.close()


connection.close()
