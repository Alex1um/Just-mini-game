import random
import glob
import pickle
import time


class City:

    def __init__(self, x, y, fractions: dict):
        """
        may be some parametrs
        :param x:
        :param y:
        """
        self.x, self.y = x, y
        self.fractions = fractions

    @classmethod
    def generate_sity(cls, fractions, most_fraction_index):
        x, y = random.randint(0, 50), random.randint(0, 50)
        while x ** 2 + y ** 2 >= 2500:
            x, y = random.randint(0, 50), random.randint(0, 50)
        table = {}
        most = random.uniform(0.5, 1)
        table[fractions[most_fraction_index]] = most
        rest = 1 - most
        for fraction in fractions[:most_fraction_index] + fractions[most_fraction_index + 1:]:
            new = rest * random.random()
            rest -= new
            table[fraction] = new
        return cls(x, y, table)

    def get_fraction(self):
        return max(self.fractions.items(), key=lambda x: x[1])[0]


class Planet:

    def __init__(self, size, name):
        sprite_num = str(random.randint(1, 32))
        if len(sprite_num) == 1:
            sprite_num = '0' + sprite_num
        self.img = f'planet_{sprite_num}.png'
        self.hd_img = f'planets_high\\planet{sprite_num}.png'
        self.map = []
        self.name = name
        self.space = []
        self.fraction = None
        self.d = size
        self.x_relative, self.y_relative = random.randint(0, 100 - size), random.randint(0, 100 - size)


class Ship:

    def __init__(self):
        self.weapons = []


class SpaceMap:

    def __init__(self, planets):
        self.planets = planets

    @classmethod
    def generate(cls, planet_count):
        planets = []
        with open('staff\\planet_names.set', 'rb') as f:
            names = pickle.load(f)
        for name in random.choices(names, k=planet_count):
            planets.append(Planet(random.randint(5, 7), name))
        return cls(planets)


class Fraction:

    def __init__(self, name):
        self.name = name

    @classmethod
    def generate_name(cls):
        return cls(str(time.time()))


class Game:
    """

    """
    def __init__(self, fractions, space_map):
        pass

    @classmethod
    def generate(cls, number_of_fraction, planet_count):
        fractions = [Fraction.generate_name() for _ in ' ' * number_of_fraction]
        space_map = SpaceMap.generate(planet_count)
