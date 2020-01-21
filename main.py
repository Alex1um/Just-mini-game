import pygame
from pygame.locals import *
pygame.init()

from engine import *
from core import *


class AAA:

    def resize(self, resolution):
        screen = pygame.display.get_surface()
        caption = pygame.display.get_caption()
        cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007
        flags = screen.get_flags()
        bits = screen.get_bitsize()
        pygame.display.init()
        screen = pygame.display.set_mode(resolution, flags, bits)
        pygame.display.set_caption(*caption)

        pygame.key.set_mods(0)  # HACK: work-a-round for a SDL bug??

        pygame.mouse.set_cursor(*cursor)  # Duoas 16-04-2007
        self.screen = screen
        for obj in self.objects:
            obj.adopt(resolution)

    def toggle_fullscreen(self):
        screen = pygame.display.get_surface()
        # tmp = screen.convert()
        caption = pygame.display.get_caption()
        cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007

        w, h = screen.get_width(), screen.get_height()
        flags = screen.get_flags()
        bits = screen.get_bitsize()

        # pygame.display.quit()
        pygame.display.init()

        screen = pygame.display.set_mode((w, h), flags ^ FULLSCREEN, bits)
        # screen.blit(tmp, (0, 0))
        pygame.display.set_caption(*caption)

        pygame.key.set_mods(0)  # HACK: work-a-round for a SDL bug??

        pygame.mouse.set_cursor(*cursor)  # Duoas 16-04-2007

        return screen

    class AAAPlanet(RadialObject):

        def __init__(self, planet: Planet, resolution):
            super().__init__(resolution, planet.x_relative, planet.y_relative, planet.d // 2)
            self.set_image(planet.img, size_mode='%obj')
            self.text_set(planet.name, (0, 255, 0), 100, 50)

    def __init__(self, sizex=None, sizey=None):
        if sizex is None and sizex == sizey:
            info_display = pygame.display.Info()
            sizex, sizey = info_display.current_w, info_display.current_h
        self.resolution = (sizex, sizey)
        self.screen = pygame.display.set_mode(self.resolution)
        self.frames = 30
        self.clock = pygame.time.Clock()
        self.planets = []
        self.sprites = pygame.sprite.Group()
        self.objects = []
        space_map = SpaceMap.generate(11)
        self.load_space_map(space_map)
        self.run()

    def load_space_map(self, space_map):
        background = Object(self.resolution, 0, 0, 100, 100)
        background.set_image(random.choice(glob.glob('galaxes\\*')), size_mode='%obj')
        self.background = background
        for planet in space_map.planets:
            self.objects.append(self.AAAPlanet(planet, self.resolution))

    def run(self):
        while 1:
            for e in pygame.event.get():
                if e.type == pygame.KEYUP:
                    if e.dict['key'] == 32:
                        self.toggle_fullscreen()
                        break
                    elif e.dict['key'] == 114:
                        resolution = tuple(map(int, input().split()))
                        self.resize(resolution)
                elif e.type == pygame.QUIT:
                    pygame.quit()
                print(e)
            self.background.draw(self.screen)
            for obj in self.objects:
                obj.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(30)


AAA(1000, 1000)