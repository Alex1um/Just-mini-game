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
        self.name = name
        self.r_rel = r_rel
        self.status = 'PEACE'
        self.squads = []
        self.fractions = set()

    def add_squad(self, squad):
        self.squads.append(squad)
        self.fractions.add(squad.get_fraction())
        if len(self.fractions) > 1:
            self.battle = Battle()

    def get_statistic(self):
        return self.fractions_impact

    def get_name(self):
        return str(self.name)

    def get_coords(self):
        return self.x_rel, self.y_rel

    def change_fraction_imact(self, fraction: Fraction, max_percent=10):
        pass

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
        self.ships = {}         # {TYPE_OF_SHIP: N_OF_SHIPS}
        self.fraction = fraction

    def get_fraction(self):
        return self.fraction

    def set_ships(self, ships: dict):
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


class Battle:
    def __init__(self):
        pass


class Ship:

    def __init__(self, name, damage, health, speed, attack_range):
        self.name = name
        self.damage = damage
        self.health = health
        self.speed = speed
        self.attack_range = attack_range

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
