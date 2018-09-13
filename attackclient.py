from threading import Thread
import socket
import attack


def connect_server(host, port, ):
    server = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    message = ''
    # system_exit will be the codeword to stop
    while message != 'system_exit':
        s.sendto(message.encode('utf-8'), server)
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Received from server: " + data)

        message

    s.close()


def Main():
    host = input("Host IP: ")
    port = input("Port: ")
    network = Thread(target = connect_server, args = (host, port))
    game = Thread(target = attack.start(), args = ())