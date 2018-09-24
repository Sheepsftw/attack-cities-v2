


class City():

    def __init__(self, loc_x, loc_y, hash):
        self.hash = hash  # a lot depends on this hash being correct, 0 to number of cities - 1
        self.loc_x = loc_x  # maybe I should make this final?
        self.loc_y = loc_y
        self.pop = 25
        # 0 means it is a neutral city
        self.owner = 0
        self.selected = False
        self.upgrade = 0
        self.in_siege = False
        self.edges = []

    def increment_pop(self):
        if not self.owned:
            return

        if self.upgrade == 1:
            self.pop += 2
        elif self.upgrade == 2:
            self.pop += 3
        else:
            self.pop += 1

    def to_string(self):
        # there's gotta be a better way
        s = "city" + " " + str(self.hash) + " " + str(self.loc_x) + " " + str(self.loc_y) + " " + \
               str(self.pop) + " " + str(self.owned) + " " + str(self.upgrade) + " " + str(self.in_siege)
        for c in s.edges:
            s += str(c.hash)
        s += "\n"
        return s


# maybe I should find a way to return # of players required for each map & starting locs
def small_test():
    cities = []
    armies = []
    city1 = City(50, 50, 0)
    city1.owned = 1
    city2 = City(300, 300, 1)
    city1.edges.append(city2)
    city2.edges.append(city1)
    city3 = City(-150, 300, 2)
    city1.edges.append(city3)
    city3.edges.append(city1)
    cities.append(city1)
    cities.append(city2)
    cities.append(city3)
    return cities