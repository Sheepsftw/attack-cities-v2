import pygame
import time
import logic
import math


class City:

    def __init__(self):
        self.edges = [] # array of cities
        self.pop = 25
        self.loc_x = 0 # coords are for top left corner of image
        self.loc_y = 0
        self.owned = False
        self.selected = False
        self.upgrade = 0 # 0 = nothing, 1 = capital, 2 = factory, 3 = fort, 4 = artillery
        self.hash = 0

    def __init__(self, loc_x, loc_y, hash):
        self.edges = []
        self.pop = 25
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.owned = False
        self.selected = False
        self.upgrade = 0
        self.hash = hash # a lot depends on this hash being correct, 0 to number of cities - 1

    def increment_pop(self):
        if not self.owned:
            return

        if self.upgrade == 1:
            self.pop += 2
        elif self.upgrade == 2:
            self.pop += 3
        else:
            self.pop += 1


class Army:

    def __init__(self):
        self.size = 1
        self.loc_x = 0
        self_loc_y = 0
        self.selected = 0
        self.direction = (0, 0)
        self.path = []
        self.owned = True
        self.img = None
        self.img_dia = 0
        self.next_city = None
        self.prev_city = None

    def __init__(self, city, size, dest):
        self.path = []
        self.size = size
        self.loc_x = city.loc_x
        self.loc_y = city.loc_y
        self.path.append(city)
        self.target(dest)
        self.prev_city = city

    # battle with an army
    def battle(self, enemy):
        temp = self.size
        s_multiplier = 1
        e_multiplier = 1
        # artillery should provide a multiplier to the damage that an army does, based on the city's population
        if self.prev_city.upgrade == 4:
            s_multiplier = math.log10(self.prev_city.pop)
        if enemy.prev_city.upgrade == 4:
            e_multiplier = math.log_10(enemy.prev_city.pop)
        self.size -= math.floor(math.max(0, math.sqrt(enemy.size)) * e_multiplier) # in case i want to reduce the attrition by some amount
        enemy.size -= math.floor(math.max(0, math.sqrt(temp)) * s_multiplier) # i hope this works

    # battle with a city
    def siege(self, enemy):
        temp = self.size
        s_multiplier = 1
        e_multiplier = 0
        if self.prev_city.upgrade == 4:
            s_multiplier = math.log10(self.prev_city.pop)
            # fort should reduce damage by a fixed amount
        if enemy.upgrade == 3:
            e_multiplier = 10
        self.size -= math.floor(math.max(0, math.sqrt(enemy.size)))
        enemy.size -= math.floor(math.max(0, math.sqrt(temp) * s_multiplier - e_multiplier))

    def target(self, end_city):
        self.path = logic.find_path(self.path[0], end_city)
        self.next_city = self.path[0]
        self.direction = (self.next_city.loc_x - self.loc_x, self.next_city.loc_y - self.loc_y)

    def resize_img(self):
        temp = self.img_dia
        if self.size < 125:
            self.img_dia = 5
        elif 125 > self.size > 27000:
            self.img_dia = math.floor(math.pow(self.size, 0.33333))
        else:
            self.img_dia = 30

        if self.img_dia != temp:
            self.img = pygame.transform.scale(self.img, (self.img_dia, self.img_dia))

    # need to figure out where to put this
    def reach_city(self):
        self.prev_city = self.path[0]
        self.path.remove(0) # not sure if this is right
        self.next_city = self.path[0]
        self.direction = (self.next_city.loc_x - self.loc_x, self.next_city.loc_y - self.loc_y)


    def stop(self):
        self.path = self.path[0]


pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('attack-cities')

clock = pygame.time.Clock()
cities = []
armies = []
q = City(50, 50, 0)
q.owned = True
r = City(300, 300, 1)
q.edges.append(r)
r.edges.append(q)
cities.append(q)
cities.append(r)

city_diameter = 30

city_img = pygame.image.load('neutral_city.jpg')
city_img = pygame.transform.scale(city_img, (city_diameter, city_diameter))
big_img = pygame.transform.scale(city_img, (city_diameter + 10, city_diameter + 10))

cities_selected = []

army_speed = 3 # maybe change army speed based on size?


def draw_selection(city):
    city_x = city.loc_x
    city_y = city.loc_y
    right_x = city_x + city_diameter
    right_y = city_y + city_diameter
    # sorry wtf?
    pygame.draw.rect(game_display, black, [city_x - 5, city_y - 5, 10, 4]) # what if big_img?
    pygame.draw.rect(game_display, black, [city_x - 5, city_y - 5, 4, 10])
    pygame.draw.rect(game_display, black, [city_x - 5, right_y + 1, 10, 4])
    pygame.draw.rect(game_display, black, [city_x - 5, right_y - 5, 4, 10])
    pygame.draw.rect(game_display, black, [right_x - 5, city_y - 5, 10, 4])
    pygame.draw.rect(game_display, black, [right_x + 1, city_y - 5, 4, 10])
    pygame.draw.rect(game_display, black, [right_x + 1, right_y - 5, 4, 10])
    pygame.draw.rect(game_display, black, [right_x - 5, right_y + 1, 10, 4])
    return


def draw_big_selection(city):
    return


def draw_armies():
    for a in armies:
        pygame.blit(game_display, a.img)
    return


def move_tick_armies():
    for a in armies:
        return


def create_army(city, size, dest):
    print("yes")
    if size > city.pop:
        size = city.pop - 1

    if size > 0:
        city.pop -= size
        new_army = Army(city, size, dest)
        armies.append(new_army)


def draw_cities(array, curr_pos):
    pop_font = pygame.font.SysFont(None, 15)
    for c in array:
        pop_text = pop_font.render(str(c.pop), True, black)

        if 0 < curr_pos[0] - c.loc_x < city_diameter and 0 < curr_pos[1] - c.loc_y < city_diameter:
            game_display.blit(big_img, (c.loc_x - 5, c.loc_y - 5))
            game_display.blit(pop_text, (c.loc_x - 5, c.loc_y - 15))  # draw the population of the city
        else:
            game_display.blit(city_img, (c.loc_x, c.loc_y)) # draw the city
            game_display.blit(pop_text, (c.loc_x, c.loc_y - 10))  # draw the population of the city
        for e in c.edges:
            pygame.draw.line(game_display, black, (c.loc_x + city_diameter / 2, c.loc_y + city_diameter / 2),
                                                    (e.loc_x + city_diameter / 2, e.loc_y + city_diameter / 2)) # draw all roads to the city, fix coords issue
        if c.selected:
            draw_selection(c) # if the city is selected, show it

    draw_armies()
    return


def increment_pop(array):
    for c in array:
        c.increment_pop()


def scroll_left():
    for c in cities:
        c.loc_x += 1


def scroll_right():
    for c in cities:
        c.loc_x -= 1


def scroll_up():
    for c in cities:
        c.loc_y += 1


def scroll_down():
    for c in cities:
        c.loc_y -= 1


def game_loop():
    game_finished = False

    send_q = 10
    send_w = 20
    send_e = 100
    send_r = 1000 # vals to send army

    selecting = False
    in_selection = False # whether or not there are cities that are selected

    select_start = (0, 0)

    pop_tick = 0

    hovered = None

    while not game_finished:

        curr_pos = pygame.mouse.get_pos()

        # figure out a way to scroll
        if 0 < curr_pos[0] < 50:
            scroll_left()
        elif display_width > curr_pos[0] > display_width - 50:
            scroll_right()

        if 0 < curr_pos[1] < 50:
            scroll_up()
        elif display_height > curr_pos[1] > display_height - 50:
            scroll_down()

        for c in cities:
            if 0 < curr_pos[0] - c.loc_x < city_diameter and 0 < curr_pos[1] - c.loc_y < city_diameter:
                hovered = c

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print("Made it!")

                # if not in_selection:
                selecting = True
                select_start = pygame.mouse.get_pos()
                # else:
                in_selection = False
                for c in cities_selected:
                    c.selected = False
                cities_selected.clear()
            elif event.type == pygame.MOUSEBUTTONUP:
                if selecting:
                    selecting = False
                    in_selection = True
                    min_x = min(select_start[0], curr_pos[0]) # this is dumb
                    min_y = min(select_start[1], curr_pos[1])
                    max_x = max(select_start[0], curr_pos[0])
                    max_y = max(select_start[0], curr_pos[0])
                    for c in cities:
                        if min_x < c.loc_x < max_x and min_y < c.loc_y < max_y:
                            if c.owned:
                                cities_selected.append(c)
                                c.selected = True

                    if len(cities_selected) < 1:
                        in_selection = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_selection = False
                    for c in cities_selected:
                        c.selected = False
                    cities_selected.clear()
                if in_selection:
                    if event.key == pygame.K_q:
                        for c in cities_selected:
                            create_army(c, send_q, hovered)
                    elif event.key == pygame.K_w:
                        for c in cities_selected:
                            create_army(c, send_w, hovered)
                    elif event.key == pygame.K_e:
                        for c in cities_selected:
                            create_army(c, send_e, hovered)
                    elif event.key == pygame.K_r:
                        for c in cities_selected:
                            create_army(c, send_r, hovered)

        pop_tick += 1
        if pop_tick == 60:
            pop_tick = 0
            increment_pop(cities)

        # print(select_start[0])

        game_display.fill(white)
        # game_display.blit(pygame.Surface(), (0, 0))

        draw_cities(cities, curr_pos)

        if selecting:
            sel_width = curr_pos[0] - select_start[0]
            sel_height = curr_pos[1] - select_start[1]

            # there has to be a better way to do this
            draw_start = select_start
            if sel_width <= 0 and sel_height <= 0:
                draw_start = curr_pos
            elif sel_width <= 0 < sel_height:
                draw_start = (curr_pos[0], select_start[1])
            elif sel_width > 0 >= sel_height:
                draw_start = (select_start[0], curr_pos[1])

            sel_width = abs(sel_width)
            sel_height = abs(sel_height)

            s = pygame.Surface((sel_width, sel_height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 20))
            game_display.blit(s, draw_start)

        pygame.display.update()

        clock.tick(60)








game_loop()
pygame.quit()
quit()
