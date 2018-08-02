


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
    q = City(50, 50, 0)
    q.owned = True
    r = City(300, 300, 1)
    q.edges.append(r)
    r.edges.append(q)
    cities.append(q)
    cities.append(r)
    return cities