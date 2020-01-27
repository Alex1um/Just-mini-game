import random
import glob
import pickle
import time
from typing import *
import utils
import uuid

SHIP_TYPES = ['destroyer', 'warp-ship', 'fat-man', 'soldier', 'long-range']
FRACTIONS = ['RED', 'BLUE']
SHIP_STATUS = ['PLANET', 'TRAVEL']


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

class Battle:
    def __init__(self, squads, fractions):
        self.stime = time()
        self.squads = squads
        self.start_coords = [500, 500]
        self.fractions = fractions
        self.ships = []
        self.bullets = []

        for squad in squads:
            for ship in squad.get_ships():
                self.ships.append({'fraction': squad.get_fraction(), 'ship': ship, 'xs': self.start_coords[0], 'ys': self.start_coords[1], 'xf': self.start_coords[0], 'yf': self.start_coords[1], 'status': 'FIXED'})
                
    def set_tick(self, tick):
        self.TICK = tick

    def get_state(self):
        ctime = time()
        d = ctime - self.stime
        TICK = self.TICK
        for i in range(int(d//TICK)):
            for k, ship in enumerate(self.ships):
                if ship['status'] == 'TRAVEL':
                    max_distance = ship['ship'].get_speed() * TICK
                    route = ((ship['xf'] - ship['xs']) ** 2 + (ship['yf'] - ship['ys']) ** 2) ** 0.5
                    if route != 0:
                        travel_progress = (max_distance / route)
                    else:
                        travel_progress = 1

                    if travel_progress < 1:
                        ship['xs'] += travel_progress * (ship['xf'] - ship['xs'])
                        ship['ys'] += travel_progress * (ship['yf'] - ship['ys'])
                    else:
                        ship['xs'] = ship['xf']
                        ship['ys'] = ship['yf']

                aims = {}
                for ind, enemy in enumerate(self.ships):
                    if ind != k:
                        dist = ((enemy['xs'] - ship['xs']) ** 2 + (enemy['ys'] - ship['ys']) ** 2) ** 0.5
                        if dist < ship['ship'].get_attack_range():
                            aims[dist] = (enemy['xs'], enemy['ys'])
                if aims:
                    aim = aims[min(aims)]
                    self.bullets.append(aim)
        self.stime = ctime
        return self.ships, self.bullets

    def change_pos(self, ship, nx, ny):
        for k, i in enumerate(self.ships):
            if i['ship'] == ship:
                i['xf'] = nx
                i['yf'] = ny
                if i['xs'] != nx or i['yf'] != ny:
                    self.ships[k]['status'] = 'TRAVEL'

    def add_squad(self, squad):
        for ship in squad.get_ships():
            self.ships.append({'fraction': squad.get_fraction(), 'ship': ship, 'xs': self.start_coords[0], 'ys': self.start_coords[1], 'xf': self.start_coords[0], 'yf': self.start_coords[1], 'status': 'FIXED'})

    def start_battle(self):
        self.stime = time()

    def escape(self, fraction):
        pass


class Planet:

    def __init__(self,
                 x_rel: int,
                 y_rel: int,
                 r_rel,
                 orbit,
                 name,
                 fractions_impact):
        self.x_rel, self.y_rel = x_rel, y_rel
        self.fractions_impact = fractions_impact
        self.orbit = orbit
        self.battle = None
        self.name = name
        self.r_rel = r_rel
        self.status = 'PEACE'
        self.squads = []
        self.fractions = set()

    def add_squad(self, squad):
        self.squads.append(squad)
        self.fractions.add(squad.get_fraction())
        if len(self.fractions) > 1:
            self.battle = Battle(self.squads, self.fractions)
            self.status = 'BATTLE'

    def get_state(self):
        return self.status

    def get_battle(self):
        return self.battle

    def get_status(self):
        stat = self.map[0].fractions
        for city in self.map[1:]:
            for k, v in city.fractions.items():
                stat[k] += v
        return stat

    def get_statistic(self):
        return self.fractions_impact

    def get_name(self):
        return str(self.name)

    def get_coords(self):
        return self.x_rel, self.y_rel

    def get_most_fraction(self):
        return max(self.get_statistic().items(), key=lambda x: x[1])[0]

    def change_fraction_imact(self, fraction: Fraction, max_percent=10):
        city_changing_impact = utils.break_number_sum(random.uniform(0, max_percent), len(self.map))
        for i in range(len(self.map)):
            self.map[i].change_fraction_impact(fraction, city_changing_impact[i])

    @classmethod
    def generate(cls,
                 diameter: int,
                 name: str,
                 fractions: Union[Tuple[Fraction], List[Fraction]],
                 most_fraction: Fraction):
        ''' may be realesed in game_area
        sprite_num = str(random.randint(1, 32))
        if len(sprite_num) == 1:
            sprite_num = '0' + sprite_num
        img = f'planet_{sprite_num}.png'
        hd_img = f'planets_high\\planet{sprite_num}.png'
        '''
        orbit: List[Ship] = []
        x_relative = random.randint(0, 100 - diameter)
        y_relative = random.randint(0, 100 - diameter)
        impact = {}
        impact[most_fraction] = random.uniform(0.5, 1)
        imp = utils.break_number_sum(1 - impact[most_fraction], len(fractions) - 1)
        most_fraction_index = fractions.index(most_fraction)
        for i, fraction in enumerate(fractions[:most_fraction_index] + fractions[most_fraction_index + 1:]):
            impact[fraction] = imp[i]
        return cls(x_relative, y_relative, diameter, orbit, name, impact)


class Squad:
    def __init__(self, planet, fraction):
        self.planet = planet
        self.status = 'PLANET'
        self.ships = []        # {TYPE_OF_SHIP: N_OF_SHIPS}
        self.fraction = fraction

    def get_fraction(self):
        return self.fraction

    def set_ships(self, ships: list):
        self.ships = ships

    def get_planet(self):
        return self.planet

    def get_ships(self):
        return self.ships

    def get_status(self):
        return self.status

    def start_travel(self, destination: Planet):
        self.status = 'TRAVEL'
        self.destination = destination
        speed = float('inf')               # count
        for i in self.ships:
            speed = min(i.get_speed(), speed)
        self.travel_time = float('inf')
        x1, y1 = self.planet.get_coords()
        x2, y2 = self.destination.get_coords()
        S = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        self.travel_time = S / speed
        return self.planet, self.destination, self.travel_time

    def finish_travel(self):
        self.planet = self.destination
        self.status = 'PLANET'


class Ship:

    def __init__(self, name, damage, health, speed, attack_range, size):
        self.size = size
        self.name = name
        self.damage = damage
        self.health = health
        self.speed = speed
        self.attack_range = attack_range

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
        for name in random.choices(names, k=planet_count):
            planets.append(Planet.generate(random.randint(*diameter),
                                           name,
                                           fractions,
                                           random.choice(fractions)))
        return cls(planets)


class Game:
    """

    """
    def __init__(self, fractions, space_map):
        self.fractions = fractions
        self.space_map = space_map

    @classmethod
    def generate(cls, number_of_fraction, planet_count):
        fractions = [Fraction(name) for name in {'red', 'green', 'blue', 'black', 'white'}]
        space_map = SpaceMap.generate(planet_count, (5, 7), fractions)
        return cls(fractions, space_map)

TICK = 0.01
ship_destroyer = Ship('destroyer', 100, 50, 250, 10, 10)
ship_destroyer2 = Ship('destroyer2', 100, 50, 250, 10, 10)
ship_speeder = Ship('speeder', 100, 50, 250, 10, 10)
planet_earth = Planet(60, 20, 5, [], 3, 'earth')
planet_mars = Planet(30, 60, 5, [], 3, 'mars')
squad1 = Squad(planet_earth, 'BLUE')
squad1.set_ships([ship_destroyer, ship_destroyer2])
squad2 = Squad(planet_earth, 'BLACK')
squad2.set_ships([ship_speeder])
planet_earth.add_squad(squad1)
planet_earth.add_squad(squad2)
print(planet_earth.get_state())
battle = planet_earth.get_battle()
battle.set_tick(TICK)
battle.change_pos(ship_destroyer2, 800, 900)

time1 = time()
o = 0
while time() - time1 < 5:
    if (time() - time1) // 0.1 != o:
        o = (time() - time1) // 0.1
        for i in battle.get_state()[0]:
            if i['ship'] == ship_destroyer2:
                print(round(time() - time1, 2), str(i['xs']) + ', ' + str(i['ys']))


'''
print(battle.get_state())

for i in battle.get_state()[0]:
            if i['ship'] == ship_destroyer2:
                print(i['xs'], i['ys'])'''

'''
print(squad1.get_status())
print(squad1.get_planet().get_name())
res = squad1.start_travel(planet_mars)
print(res[0].get_name())
print(res[1].get_name())
print(res[2])
print(squad1.get_status())
squad1.finish_travel()
print(squad1.get_planet().get_name())

print(ship_destroyer.get_name())
print(ship_destroyer.get_damage())
print(ship_destroyer.get_health())
print(ship_destroyer.get_speed())
print(ship_destroyer.get_attack_range())'''