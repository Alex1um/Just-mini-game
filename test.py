import random
import glob
import pickle


class Planet:

    def __init__(self, size, name):
        sprite_num = str(random.randint(1, 32))
        if len(sprite_num) == 1:
            sprite_num = '0' + sprite_num
        self.img = glob.glob(f'planets\\planet_{sprite_num}.png')[0]
        self.hd_img = glob.glob(f'planets_high\\planet{sprite_num}.png')
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
        background = random.choice(glob.glob('galaxes\\*'))
        for name in random.choices(names, k=planet_count):
            planets.append(Planet(random.randint(5, 7), name))
        return cls(planets)