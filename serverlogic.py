import play_board
import math

class BoardState:

    # record which client it came from
    def __init__(self, player, string_state = None):
        # -1 means it is the server board
        self.player = player
        self.cities = []
        self.armies = []
        self.battles = []
        if string_state is not None:
            self.convert_string_to_state(string_state)

    def convert_string_to_state(self, string):
        return


# the plan is to receive a board state, merge with server state, return merged state
def merge(player_state, server_state):
    ret = BoardState()
    # STABLE CODE
    for city_index in range(0, len(server_state.cities)):
        c_player = player_state.cities[city_index]
        c_server = player_state.cities[city_index]
        c = play_board.City(c_server.loc_x, c_server.loc_y, c_server.hash)
        if c_player.owner == player_state.player:
            c.pop = c_player.pop
        c.pop = math.ceil((c_player.pop + c_server.pop) / 2)
    # armies is a bit harder
    for army_index in range(0, len(server_state.armies)):
        break
    return ret
