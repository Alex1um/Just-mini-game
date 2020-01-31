import random
import glob
import pickle
from time import time, sleep
from typing import *
import utils
import uuid
from threading import Thread

SHIP_TYPES = ['destroyer', 'warp-ship', 'fat-man', 'soldier', 'long-range']
FRACTIONS = ['RED', 'BLUE']
SHIP_STATUS = ['PLANET', 'TRAVEL']


def timer(delay, foo):
    sleep(delay)
    foo()


class Fraction:

    def __init__(self, name):
        self.name = name

    @classmethod
    def generate_name(cls):
        return cls(str(uuid.uuid4()))

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Planet:

    def __init__(self,
                 x_rel: int,
                 y_rel: int,
                 r_rel,
                 name,
                 fractions_impact,
                 produce_ship,
                 produce_timer):
        self.x_rel, self.y_rel = x_rel, y_rel
        self.fractions_impact: Dict[Fraction, float] = fractions_impact
        self.name = name
        self.r_rel = r_rel
        self.status = 'PEACE'
        self.squads: List[Squad] = []
        self.produce_ship: Callable = produce_ship
        self.produce_timer = produce_timer
        self.battle = Battle(self)
        Thread(target=self.produce).start()

    def produce(self):
        while 1:
            sleep(self.produce_timer)
            if not self.squads:
                sq = Squad(self)
                sq.set_ships({self.produce_ship()})
                self.add_squad(sq)
            else:
                for i in range(len(self.squads)):
                    if len(self.squads[i].ships) <= 3:
                        self.squads[i].ships.add(self.produce_ship())
            self.battle.update_squads()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def add_squad(self, squad):
        squad.planet = self
        squad.status = self.status
        self.squads.append(squad)
        self.battle.add_squad(squad)
        if len(self.fractions()) > 1:
            self.battle.set_status('BATTLE')

    def fractions(self):
        return set(map(lambda x: x.fraction, self.squads))

    def del_squad(self, squad):
        self.squads.remove(squad)

    def get_state(self):
        return self.status

    def get_battle(self):
        return self.battle

    def get_statistic(self):
        return self.fractions_impact

    def get_name(self):
        return str(self.name)

    def get_coords(self):
        return self.x_rel, self.y_rel

    def get_most_fraction(self):
        return max(self.get_statistic().items(), key=lambda x: x[1])[0]

    def change_fraction_imact(self, fraction: Fraction, max_percent=50):
        max_fract = self.get_most_fraction()
        self.fractions_impact[fraction] += max_percent / 100
        val = 0
        for fract, v in sorted(self.fractions_impact.items(), key=lambda x: x[1])[:-1]:
            if fract != fraction:
                r = random.uniform(0, v)
                val += r
                self.fractions_impact[fract] -= random.uniform(0, r)
        self.fractions_impact[max_fract] -= (100 - max_percent) / 100 - val

    @classmethod
    def generate(cls,
                 radius: int,
                 name: str,
                 fractions: Union[Tuple[Fraction], List[Fraction]],
                 most_fraction: Fraction,
                 x,
                 y):
        ''' may be realesed in game_area
        sprite_num = str(random.randint(1, 32))
        if len(sprite_num) == 1:
            sprite_num = '0' + sprite_num
        img = f'planet_{sprite_num}.png'
        hd_img = f'planets_high\\planet{sprite_num}.png'
        '''
        x_relative = x
        y_relative = y
        # x_relative = random.randint(0, 100 - radius * 2)
        # y_relative = random.randint(0, 100 - radius * 2)
        impact = {}
        impact[most_fraction] = random.uniform(0.5, 1)
        imp = utils.break_number_sum(1 - impact[most_fraction], len(fractions) - 1)
        most_fraction_index = fractions.index(most_fraction)
        produce_ship = random.choice(SHIPS)
        produce_timer = 1
        for i, fraction in enumerate(fractions[:most_fraction_index] + fractions[most_fraction_index + 1:]):
            impact[fraction] = imp[i]
        return cls(x_relative, y_relative, radius, name, impact, produce_ship, produce_timer)


class Squad:
    def __init__(self, planet: Planet, fraction=None):
        self.planet = planet
        self.id = str(uuid.uuid4())
        self.status = 'PEACE'
        self.ships = set()        # {TYPE_OF_SHIP: N_OF_SHIPS}
        self.fraction = fraction if fraction else planet.get_most_fraction()

    def merge(self, other):
        if self.status == 'PEACE':
            self.ships |= other.ships

    def __repr__(self):
        return self.id

    def __str__(self):
        return f'{self.id}: {self.ships}'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def get_fraction(self):
        return self.fraction

    def set_ships(self, ships: set):
        self.ships = ships

    def get_planet(self):
        return self.planet

    def get_ships(self):
        return self.ships

    def get_status(self):
        return self.status

    def start_travel(self, destination: Planet):
        if self.status != 'BATTLE':
            self.planet.del_squad(self)
            self.status = 'TRAVEL'
            speed = float('inf')               # count
            for i in self.ships:
                speed = min(i.get_speed(), speed)
            self.travel_time = float('inf')
            x1, y1 = self.planet.get_coords()
            x2, y2 = destination.get_coords()
            S = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            self.travel_time = S / speed * 100
            # self.travel_time = 1  # todo: remove this line

            def travel(planet: Planet, destination: Planet, squad: Squad):
                destination.add_squad(squad)

            Thread(target=timer, args=(self.travel_time, lambda: travel(self.planet, destination, self))).start()
            return self.planet, destination, self.travel_time
        return None, None, None


class Battle:
    def __init__(self, planet: Planet):
        self.stime = time()
        self.planet = planet
        self.size = (10000, 10000)
        self.ships = []
        self.bullets = []
        self.status = 'PEACE'
        self.set_tick(0.01)
        Thread(target=self.get_state).start()

    def update_squads(self):
        if self.ships:
            ships = set(map(lambda x: x['ship'], self.ships))
            check = set()
            i = 0
            while i < len(self.planet.squads):
                new_ships = set(self.planet.squads[i].ships) & ships
                if new_ships:
                    check |= new_ships
                    self.planet.squads[i].set_ships(new_ships)
                    i += 1
                else:
                    del self.planet.squads[i]
            self.ships = list(filter(lambda x: x['ship'] in check, self.ships))

    def add_squad(self, squad):
        for ship in squad.ships:
            self.ships.append(self.parse_ship(ship, squad.fraction))
        if not self.win():
            self.set_status('BATTLE')

    def win(self):
        return len(set(ship['fraction'] for ship in self.ships)) == 1

    def parse_ship(self, ship, fraction):
        return {'fraction': fraction,
                'ship': ship,
                'health': ship.get_health(),
                'xs': random.randint(100, self.size[0]),
                'ys': random.randint(100, self.size[1]),
                'xf': random.randint(100, self.size[0]),
                'yf': random.randint(100, self.size[1]),
                'status': 'FIXED',
                'reload': time(),
                'size': ship.get_size(),
                'max_health': ship.max_health,
                'img': ship.img}

    def set_tick(self, tick):
        self.TICK = tick

    def get_state(self):
        BULLET_SPEED = 1000

        def hit(x1, y1, x0, y0, r):
            return (x0 - x1) ** 2 + (y0 - y1) ** 2 <= r ** 2

        while 1:
            fractions = set()
            for k, ship in enumerate(self.ships):
                fractions.add(ship['fraction'])
                if ship['health'] <= 0:
                    del self.ships[k]
                    continue
                if ship['status'] == 'TRAVEL':
                    max_distance = ship['ship'].get_speed() * self.TICK
                    route = ((ship['xf'] - ship['xs']) ** 2 + (
                                ship['yf'] - ship['ys']) ** 2) ** 0.5
                    if route != 0:
                        travel_progress = (max_distance / route)
                    else:
                        travel_progress = 1

                    if travel_progress < 1:
                        ship['xs'] += travel_progress * (
                                    ship['xf'] - ship['xs'])
                        ship['ys'] += travel_progress * (
                                    ship['yf'] - ship['ys'])
                    else:
                        ship['xs'] = ship['xf']
                        ship['ys'] = ship['yf']

                shoot = time()
                if (shoot - ship['reload']) >= ship['ship'].get_reload():
                    ship['reload'] = shoot
                    aims = {}
                    for ind, enemy in enumerate(self.ships):
                        if ind != k:
                            dist = ((enemy['xs'] - ship['xs']) ** 2 + (
                                        enemy['ys'] - ship[
                                    'ys']) ** 2) ** 0.5
                            if dist < ship['ship'].get_attack_range() and ship['fraction'] != enemy['fraction']:
                                # coef = ship['ship'].get_attack_range() / dist if dist != 0 else 1
                                coef = 10
                                aims[dist] = {'range': ship[
                                                  'ship'].get_attack_range(),
                                              'damage': ship[
                                                  'ship'].get_damage(),
                                              'xs': ship['xs'],
                                              'ys': ship['ys'],
                                              'xf': enemy['xs'] + (enemy['xs'] - ship['xs']) * coef,
                                              'yf': enemy['ys'] + (enemy['ys'] - ship['ys']) * coef,
                                              'killed': False,
                                              'fraction': ship['fraction']}
                    if aims:
                        aim = aims[min(aims)]
                        self.bullets.append(aim)

            for c, bullet in enumerate(self.bullets):
                if bullet['killed']:
                    continue
                for q, w in enumerate(self.ships):
                    if hit(bullet['xs'], bullet['ys'], w['xs'], w['ys'], w['size'] * 50) and bullet['fraction'] != w['fraction']:
                        self.ships[q]['health'] -= bullet['damage']
                        self.bullets[c]['killed'] = True
                        break
                if -1 >= bullet['xs'] >= self.size[0] or -1 >= bullet['ys'] >= self.size[1]:
                    self.bullets[c]['killed'] = True
                    break
                max_distance = BULLET_SPEED * self.TICK
                route = ((bullet['xf'] - bullet['xs']) ** 2 + (
                            bullet['yf'] - bullet['ys']) ** 2) ** 0.5
                # max_distance = min(bullet['range'], max_distance)
                if route != 0:
                    travel_progress = (max_distance / route)
                else:
                    travel_progress = 1

                # if travel_progress < 1:
                # self.bullets[c]['range'] -= max_distance
                self.bullets[c]['xs'] += travel_progress * (
                            bullet['xf'] - bullet['xs'])
                self.bullets[c]['ys'] += travel_progress * (
                            bullet['yf'] - bullet['ys'])
                # else:
                #     self.bullets[c]['xs'] = bullet['xf']
                #     self.bullets[c]['ys'] = bullet['yf']

            self.ships = list(filter(lambda x: x['health'] > 0, self.ships))
            self.bullets = list(filter(lambda x: not x['killed'], self.bullets))
            self.update_squads()
            sleep(self.TICK)
            if self.win() and self.status == 'BATTLE':
                self.set_status('PEACE')
                self.planet.change_fraction_imact(self.ships[0]['fraction'])

    def set_status(self, status):
        self.planet.status = status
        self.status = status
        for i in range(len(self.planet.squads)):
            self.planet.squads[i].status = status

    def change_pos(self, ship, nx, ny):
        nx, ny = round(nx * 10000), round(ny * 10000)
        for k, i in enumerate(self.ships):
            if i['ship'] == ship:
                i['xf'] = nx
                i['yf'] = ny
                if i['xs'] != nx or i['yf'] != ny:
                    self.ships[k]['status'] = 'TRAVEL'

    def start_battle(self):
        self.stime = time()

    def escape(self, fraction):
        pass


class Ship:

    def __init__(self, name, damage, health, speed, attack_range, reload_time, size, img):
        self.size = size
        self.img = img
        self.name = name
        self.damage = damage
        self.health = health
        self.id = str(uuid.uuid4())
        self.speed = speed
        self.attack_range = attack_range
        self.reload = reload_time
        self.max_health = health

    def __eq__(self, other):
        if other:
            return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def get_reload(self):
        return self.reload

    def get_size(self):
        return self.size

    def get_name(self):
        return self.name

    def get_speed(self):
        return self.speed

    def get_health(self):
        return self.health

    def get_attack_range(self):
        return self.attack_range

    def get_damage(self):
        return self.damage


class SpaceMap:
    """
    #todo realize my methods:
    flight between planets
    """

    def __init__(self, planets):
        self.planets = planets

    @classmethod
    def generate(cls,
                 planet_count,
                 diameter: Tuple[int, int],
                 fractions):
        planets = []
        with open('staff\\planet_names.set', 'rb') as f:
            names = pickle.load(f)
        counter = planet_count
        names = random.choices(names, k=planet_count)
        was = set()
        rand = (max(diameter), 100 - max(diameter) - 5)
        while counter > 0:
            x, y = random.randint(*rand), random.randint(*rand)
            for x1, y1 in was:
                if abs(x - x1) + abs(y1 - y) <= 20:
                    break
            else:
                planets.append(Planet.generate(random.randint(*diameter),
                                               names[counter - 1],
                                               fractions,
                                               random.choice(fractions),
                                               x,
                                               y,))
                counter -= 1
                was.add((x, y))
        return cls(planets)


class Game:
    def __init__(self, fractions, space_map):
        self.fractions = fractions
        self.space_map = space_map
        self.TICK = 0.01

    @classmethod
    def generate(cls, number_of_fraction, planet_count):
        fractions = [Fraction(name) for name in {'red', 'green', 'blue', 'black', 'white'}]
        space_map = SpaceMap.generate(planet_count, (5, 7), fractions)
        return cls(fractions, space_map)


ship_destroyer = lambda: Ship('destroyer', 100, 500, 1000, 100000, 10, 10, 'Communicationship_blue.png')
ship_destroyer2 = lambda: Ship('destroyer2', 100, 500, 1000, 100000, 10, 10, 'mothership_try.png')
ship_speeder = lambda: Ship('speeder', 10, 500, 3000, 10000000, 30, 5, 'alienship_new_red_try.png')
SHIPS = (ship_destroyer, ship_destroyer2, ship_speeder)
# planet_earth = Planet(60, 20, 5, [], 3, 'earth')
# planet_mars = Planet(30, 60, 5, [], 3, 'mars')
# squad1 = Squad(planet_earth, 'BLUE')
# squad1.set_ships([ship_destroyer2])
# squad2 = Squad(planet_earth, 'BLACK')
# squad2.set_ships([ship_destroyer])
# planet_earth.add_squad(squad1)
# planet_earth.add_squad(squad2)
# print(planet_earth.get_state())
# battle = planet_earth.get_battle()
# battle.set_tick(TICK)
# battle.change_pos(ship_destroyer2, 800, 900)
#
# time1 = time()
# o = 0
# while time() - time1 < 1.2:
#     p = 0'''
# '''
#     if (time() - time1) // 0.1 != o:
#         o = (time() - time1) // 0.1
#         for i in battle.get_state()[0]:
#             if i['ship'] == ship_destroyer2:
#                 print(round(time() - time1, 2), str(i['xs']) + ', ' + str(i['ys']))'''
# '''print(battle.get_state())'''
#
#
# '''
# print(battle.get_state())
#
# for i in battle.get_state()[0]:
#             if i['ship'] == ship_destroyer2:
#                 print(i['xs'], i['ys'])'''
#
# '''
# print(squad1.get_status())
# print(squad1.get_planet().get_name())
# res = squad1.start_travel(planet_mars)
# print(res[0].get_name())
# print(res[1].get_name())
# print(res[2])
# print(squad1.get_status())
# squad1.finish_travel()
# print(squad1.get_planet().get_name())
#
# print(ship_destroyer.get_name())
# print(ship_destroyer.get_damage())
# print(ship_destroyer.get_health())
# print(ship_destroyer.get_speed())
# print(ship_destroyer.get_attack_range())'''