import pygame
import logic
import math
import board



def normalize(direction):
    square = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
    if square == 0:
        return direction
    new_dir = (direction[0] / square, direction[1] / square)
    return new_dir


class Army:

    # eventually have to get multiple constructors to work. for now lets just remove this
    """
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
    """

    def __init__(self, city, size, dest):
        self.in_battle = False
        self.in_siege = False
        self.direction = (0, 0)
        self.next_city = None
        self.path = []
        self.size = size
        self.loc_x = city.loc_x
        self.loc_y = city.loc_y
        self.path.append(city)
        self.target(dest)
        self.prev_city = city
        self.enemy_army = None
        self.owned = True

    def target(self, end_city):
        self.path = logic.find_path(self.path[0], end_city, cities)
        self.next_city = self.path[0]
        self.direction = normalize((self.next_city.loc_x - self.loc_x, self.next_city.loc_y - self.loc_y))

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

    def check_city(self):
        dist_x = (self.loc_x - self.path[0].loc_x) ** 2
        dist_y = (self.loc_y - self.path[0].loc_y) ** 2
        dist = math.sqrt(dist_x + dist_y)
        if dist <= 5:
            self.reach_city()

    # need to figure out where to put this
    def reach_city(self):
        self.prev_city = self.path.pop(0)  # not sure if this is right
        if self.path:
            self.next_city = self.path[0]
            self.direction = normalize((self.next_city.loc_x - self.loc_x, self.next_city.loc_y - self.loc_y))
        else:
            if self.prev_city.owned:
                self.prev_city.pop += self.size
                self.size = 0
                armies.remove(self)
            else:
                self.in_siege = True  # problem: what if unit encounters enemy city on way there?
                sieges.append(Siege(self, self.prev_city))

    def stop(self):
        self.path = self.path[0]


class Battle:

    def __init__(self, army1, army2):
        self.army1 = army1
        self.army2 = army2

    def attrition_tick(self):
        temp = self.army1.size
        a1_multiplier = 1
        a2_multiplier = 1
        # artillery should provide a multiplier to the number of enemies killed
        # scaling off of city size
        if self.army1.prev_city.upgrade == 4:
            a1_multiplier = math.log10(self.army1.prev_city.pop)
        if self.army2.prev_city.upgrade == 4:
            a2_multiplier = math.log10(self.army2.prev_city.pop)
        self.army1.size -= math.floor(math.sqrt(self.army2.size) * a2_multiplier)  # gotta make sure armysize > 0
        self.army2.size -= math.floor(math.sqrt(temp) * a1_multiplier)
        self.check_victory()

    def check_victory(self):
        if self.army1.size <= 0:
            armies.remove(self.army1)
            if self.army2.size <= 0:
                armies.remove(self.army2)
            else:
                self.army2.in_battle = False
            battles.remove(self)
            return
        if self.army2.size <= 0:
            armies.remove(self.army2)
            self.army1.in_battle = False
            battles.remove(self)
            return


class Siege:

    def __init__(self, army, city):
        self.army = army
        self.city = city

    def attrition_tick(self):
        temp = self.army.size
        a_multiplier = 1
        c_multiplier = 0
        # fort should reduce the number of people killed by a flat amount,
        # good early but bad late
        if self.army.prev_city.upgrade == 4:
            a_multiplier = math.log10(self.army.prev_city.pop)
        if self.city.upgrade == 3:
            c_multiplier = 10
        self.army.size -= math.floor(math.sqrt(self.city.pop))
        self.city.pop -= math.floor(math.sqrt(temp) * a_multiplier - c_multiplier)
        self.check_victory()

    def check_victory(self):
        if self.army.size <= 0:
            armies.remove(self.army)
            sieges.remove(self)  # ????
            return
        if self.city.pop <= 0:
            self.city.owned = self.army.owned  # will need to change this to a number if (ever) multiplayer
            self.city.pop = self.army.size
            armies.remove(self.army)
            sieges.remove(self)



pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

display_width = 800
display_height = 600
game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('attack-cities')

clock = pygame.time.Clock()
cities = board.small_test()
armies = []
battles = []
sieges = []


city_diameter = 30

city_img = pygame.image.load('neutral_city.jpg')
city_img = pygame.transform.scale(city_img, (city_diameter, city_diameter))
big_img = pygame.transform.scale(city_img, (city_diameter + 10, city_diameter + 10))
army_img = pygame.transform.scale(city_img, (5, 5))

cities_selected = []

army_speed = 1 # maybe change army speed based on size?


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
    size_font = pygame.font.SysFont(None, 15)
    for a in armies:
        size_text = size_font.render(str(a.size), True, black)
        game_display.blit(army_img, (a.loc_x, a.loc_y))
        game_display.blit(size_text, (a.loc_x - 5, a.loc_y - 5))
    return


def move_tick_armies():
    for a in armies:
        if a.size <= 0:
            armies.remove(a) # dont think i need this but just in case
        if not a.in_battle and not a.in_siege:
            a.loc_x += a.direction[0] * army_speed
            a.loc_y += a.direction[1] * army_speed
            a.check_city()
        # might need to do something with army battles here, idk


def battle_tick():
    for b in battles:
        b.attrition_tick()


def siege_tick():
    for s in sieges:
        s.attrition_tick()


def create_army(city, size, dest):
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
    for a in armies:
        a.loc_x += 1


def scroll_right():
    for c in cities:
        c.loc_x -= 1
    for a in armies:
        a.loc_x -= 1


def scroll_up():
    for c in cities:
        c.loc_y += 1
    for a in armies:
        a.loc_y += 1


def scroll_down():
    for c in cities:
        c.loc_y -= 1
    for a in armies:
        a.loc_y -= 1


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

        is_hover = False

        for c in cities:
            if 0 < curr_pos[0] - c.loc_x < city_diameter and 0 < curr_pos[1] - c.loc_y < city_diameter:
                hovered = c
                is_hover = True

        if not is_hover:
            hovered = None

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
                    min_x = min(select_start[0], curr_pos[0])  # this is dumb
                    min_y = min(select_start[1], curr_pos[1])
                    max_x = max(select_start[0], curr_pos[0])
                    max_y = max(select_start[1], curr_pos[1])
                    print(str(min_x) + " " + str(min_y))
                    print(str(max_x) + " " + str(max_y))
                    print(str(cities[2].loc_x) + " " + str(cities[2].loc_y))
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
                        if hovered is not None:
                            for c in cities_selected:
                                create_army(c, send_q, hovered)
                    elif event.key == pygame.K_w:
                        if hovered is not None:
                            for c in cities_selected:
                                create_army(c, send_w, hovered)
                    elif event.key == pygame.K_e:
                        if hovered is not None:
                            for c in cities_selected:
                                create_army(c, send_e, hovered)
                    elif event.key == pygame.K_r:
                        if hovered is not None:
                            for c in cities_selected:
                                create_army(c, send_r, hovered)


        # print(str(len(sieges)))

        game_display.fill(white)
        # game_display.blit(pygame.Surface(), (0, 0))

        move_tick_armies()

        pop_tick += 1
        if pop_tick == 60:
            pop_tick = 0
            increment_pop(cities)
            battle_tick()
            siege_tick()

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
