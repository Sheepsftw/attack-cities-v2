


class City():

    def __init__(self, loc_x, loc_y, hash):
        self.edges = []
        self.pop = 25
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.owned = False
        self.selected = False
        self.upgrade = 0
        self.hash = hash  # a lot depends on this hash being correct, 0 to number of cities - 1

    def increment_pop(self):
        if not self.owned:
            return

        if self.upgrade == 1:
            self.pop += 2
        elif self.upgrade == 2:
            self.pop += 3
        else:
            self.pop += 1



def small_test():
    cities = []
    armies = []
    city1 = City(50, 50, 0)
    city1.owned = True
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