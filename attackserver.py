import socket
import sys
import play_board
import threading
import serverlogic

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = 'localhost'
port = 8080
sock.bind((host, port))
print('Server started')

player_count = 0
max_player_count = 2
cities = play_board.small_test()
player_ips = []
connections = []


class PlayerConnection(threading.Thread):
    def __init__(self, player_address):
        threading.Thread.__init__(self)
        self.address = player_address

    def run(self):
        return


def players_connect():
    global player_count
    while player_count < max_player_count:
        data, address = sock.recvfrom(1024)
        data = data.decode('utf-8')
        print("Message from: " + str(address))
        print("From connected user: " + data)
        # should probably improve this, add checks and stuff
        if address not in player_ips:
            player_count += 1
            player_ips.append(address)
            data = str(player_count)
            print("Sending: " + data)
            sock.sendto(data.encode('utf-8'), address)
        else:
            data = "Waiting for more players...\n"
            print("Sending: " + data)
            sock.sendto(data.encode('utf-8'), address)

    for address in player_ips:
        p = PlayerConnection(address)
        p.run()
        connections.append(p)


# get a better name
def run_game():
    server_state = serverlogic.BoardState()
    while True:
        data, address = sock.recvfrom(1024)
        player_number = player_ips.index(address) # i dunno man
        data = data.decode('utf-8')
        # i think i might just turn all of these to neutral? or maybe static
        if data == 'disconnect_player':
            return
        else:
            b = serverlogic.BoardState(player_number, data)
            # might wanna put this in a thread later
            server_state = serverlogic.merge(b, server_state)
            data = state_to_string(server_state)
            sock.sendto(data.encode('utf-8'), address)
        break
    sock.close()


def state_to_string():
    return ""