from threading import Thread
import socket
import attack
import player


def connect_server(host, port):
    server = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    message = 'game_init'
    # system_exit will be the codeword to stop
    while message != 'system_exit':
        s.sendto(message.encode('utf-8'), server)
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Received from server: " + data)
        if data == "Waiting for more players...\n":
            continue
        message = player.send_game_state()

    end_message = 'disconnect_player'
    s.sendto(end_message.encode('utf-8'), server)
    message = s.recvfrom(1024)
    s.close()
    print("system exit successful")


def Main():
    host = input("Host IP: ")
    port = input("Port: ")
    network = Thread(target=connect_server, args=(host, port))
    game = Thread(target=player.start(), args=())


def string_to_board_state(message):
    allobjects = message.split("\n")
