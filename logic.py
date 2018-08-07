
import math
import board


class Path:

    def __init__(self, city_array):
        self.path = city_array

    def add(self, city):
        self.path.append(city)

    def to_string(self):
        ret = ""
        for c in self.path:
            ret += str(c.hash) + " "
        return ret

    def clear(self):
        self.path.clear()


# make a new class called board with City() as a class and then import board on both scripts

def to_string(l):
    ret = ""
    for c in l:
        ret += str(c.hash) + " "
    return ret


def find_path(start_city, end_city):
    print(end_city.hash)
    cities = board.small_test()
    visited = []
    vals = []
    paths = []
    # really need to find a way to change this
    for a in range(0, len(cities)):
        vals.append(float('inf'))
        visited.append(False)
        paths.append(Path([]))
    vals[start_city.hash] = 0
    paths[start_city.hash] = Path([start_city])
    return dijkstra(start_city, end_city, visited, vals, paths, cities)


def dijkstra(start_city, end_city, visited, vals, paths, cities):
    # dont like this
    if start_city.hash == end_city.hash:
        return paths[end_city.hash].path
    visited[start_city.hash] = True
    for e in start_city.edges:
        if visited[e.hash]:
            continue
        temp_dist = vals[start_city.hash] + calc_dist(start_city, e)
        if vals[e.hash] > temp_dist:
            vals[e.hash] = temp_dist
            paths[e.hash].clear()
            paths[e.hash] = Path(paths[start_city.hash].path)
            paths[e.hash].add(e)
    q = paths[start_city.hash]
    print(str(start_city.hash) + ": " + q.to_string())
    # find the next closest city to our visited
    lowest_val = float('inf')
    temp = -1
    for a in range(0, len(vals)):
        if not visited[a] and vals[a] < lowest_val:
            lowest_val = vals[a]
            temp = a

    return dijkstra(cities[temp], end_city, visited, vals, paths, cities)


def calc_dist(city1, city2):
    return math.sqrt((city1.loc_x - city2.loc_x) ** 2 + (city1.loc_y - city2.loc_y) ** 2)