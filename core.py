import random
import glob


class Planet:

    def __init__(self, size):
        sprite_num = str(random.randint(1, 32))
        if len(sprite_num) == 1:
            sprite_num = '0' + sprite_num
        self.img = glob.glob(f'planets\\planet_{sprite_num}.png')[0]
        self.hd_img = glob.glob(f'planets_high\\planet{sprite_num}.png')
        self.map = []
        self.space = []
        self.fraction = None
        self.d = size
        self.x_relative, self.y_relative = random.randint(0, 100 - size), random.randint(0, 100 - size)


class Ship:

    def __init__(self):
        self.weapons = []


class SpaceMap:

    def __init__(self, planet_count):
        self.planets = []
        self.background = random.choice(glob.glob('galaxes\\*'))
        for _ in '?' * planet_count:
            self.planets.append(Planet(random.randint(2, 4)))