import random
import glob
import pickle
import time
from typing import *
import utils

SHIP_TYPES = ['destroyer', 'warp-ship', 'fat-man', 'soldier', 'long-range']
FRACTIONS = ['RED', 'BLUE']
SHIP_STATUS = ['PLANET', 'TRAVEL']

class Fraction:

    def __init__(self, name):
        self.name = name

    @classmethod
    def generate_name(cls):
        return cls(str(time.time()))

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()


class City:

    def __init__(self, x_relative: int, y_relative: int, stat: Dict[Fraction, int]):
        """
        # todo realize unit production
        :param x:
        :param y:
        """
        self.x_rel, self.y_rel = x_relative, y_relative
        self.fractions = stat
        self.available_for_build = []

    @classmethod
    def generate_sity(cls, fractions: Union[Tuple[Fraction], List[Fraction]], most_fraction: Fraction):
        x, y = random.randint(0, 50), random.randint(0, 50)
        while x ** 2 + y ** 2 >= 2500:  # city position on planet
            x, y = random.randint(0, 50), random.randint(0, 50)
        stat = {}  # % of fractions impact
        most = random.uniform(0.5, 1)  # most fraction
        stat[most_fraction] = most
        rest = 1 - most
        most_fraction_index = fractions.index(most_fraction)
        for fraction in fractions[:most_fraction_index] + fractions[most_fraction_index + 1:]:  # calculate other fractions impact
            new = rest * random.random()
            rest -= new
            stat[fraction] = new
        return cls(x, y, stat)

    def get_fraction(self):
        return max(self.fractions.items(), key=lambda x: x[1])[0]

    def change_fraction_impact(self, mutable_fraction: Fraction, percent: int):
        self.fractions[mutable_fraction] += percent
        fractions_changing_impact = utils.break_number_sum(percent, len(self.fractions) - 1)
        i = 0
        for fraction in self.fractions.keys():
            if fraction != mutable_fraction:
                self.fractions[fraction] -= fractions_changing_impact[i]
                i += 1

class Battle:
    def __init__(self, squads, fractions):
        self.squads = squads
        start_coords = [0.0, 0.0]
        self.fractions = fractions
        self.state = {}

        for fraction in self.fractions:
            self.state[fraction] = {}

        for squad in squads:
            for ship in squad.get_ships():
                if ship in self.state[squad.get_fraction()]:
                    self.state[squad.get_fraction()][ship]['n'] += squad.get_ships[ship]
                else:
                    self.state[squad.get_fraction()][ship] = {'n': squad.get_ships[ship], 'x': start_coords[0], 'y': start_coords[1]}
                
    
    def get_state(self):
        return self.state

    def change_pos(self, fraction, ship, nx, ny):
        self.state[fraction]][ship]['x'] = nx
        self.state[fraction]][ship]['y'] = ny

    def add_squad(self, squad):
        pass

    def start_battle(self):
        pass

    def escape(self, fraction):
        pass


class Planet:

    def __init__(self, x_rel: int, y_rel: int, r_rel, _map: List[City], orbit, name):
        self.x_rel, self.y_rel = x_rel, y_rel
        self.map = _map
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
            self.battle = Battle(self.squads, self.fractions)
            self.status = 'BATTLE'
    
    def get_battle(self):
        return self.battle

    def get_status(self):
        stat = self.map[0].fractions
        for city in self.map[1:]:
            for k, v in city.fractions.items():
                stat[k] += v
        return stat

    def get_name(self):
        return str(self.name)

    def get_coords(self):
        return self.x_rel, self.y_rel

    def get_most_fraction(self):
        return max(self.get_stat().items(), key=lambda x: x[1])[0]

    def change_fraction_imact(self, fraction: Fraction, max_percent=10):
        city_changing_impact = utils.break_number_sum(random.uniform(0, max_percent), len(self.map))
        for i in range(len(self.map)):
            self.map[i].change_fraction_impact(fraction, city_changing_impact[i])

    @classmethod
    def generate(cls,
                 diameter: int,
                 name: str,
                 fractions: Union[Tuple[Fraction], List[Fraction]],
                 most_fraction: Fraction,
                 city_count: int):
        ''' may be realesed in game_area
        sprite_num = str(random.randint(1, 32))
        if len(sprite_num) == 1:
            sprite_num = '0' + sprite_num
        img = f'planet_{sprite_num}.png'
        hd_img = f'planets_high\\planet{sprite_num}.png'
        '''
        map = [City.generate_sity(fractions, most_fraction) for _ in ' ' * city_count]
        orbit = []
        x_relative = random.randint(0, 100 - diameter)
        y_relative = random.randint(0, 100 - diameter)
        return cls(x_relative, y_relative, diameter, map, orbit, name)

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

    def start_travel(self, destination):
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
                 fractions,
                 city_count: Tuple[int, int]):
        planets = []
        with open('staff\\planet_names.set', 'rb') as f:
            names = pickle.load(f)
        for name in random.choices(names, k=planet_count):
            planets.append(Planet.generate(random.randint(*diameter),
                                           name,
                                           fractions,
                                           random.choice(fractions),
                                           random.randint(*city_count)))
        return cls(planets)


class Game:
    """

    """
    def __init__(self, fractions, space_map):
        self.fractions = fractions
        self.space_map = space_map

    @classmethod
    def generate(cls, number_of_fraction, planet_count):
        fractions = [Fraction.generate_name() for _ in ' ' * number_of_fraction]
        space_map = SpaceMap.generate(planet_count, (5, 7), fractions, (1, 5))
        return cls(fractions, space_map)


'''
ship_destroyer = Ship('destroyer', 100, 50, 250, 10)
planet_earth = Planet(60, 20, 5, [], 3, 'earth')
planet_mars = Planet(30, 60, 5, [], 3, 'mars')
squad1 = Squad(planet_earth)
squad1.set_ships({ship_destroyer: 10})
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