import pygame

# this will be where all of the visualization client-side will take place

class Player:
    def __init__(self, team):
        self.team = team
        self.can_win = True

# this will be main game loop client-side
def start():
    pygame.init()
    return


# attackclient.py will call this to find out the client game state and send to server
def send_game_state():
    return

