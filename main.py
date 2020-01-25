from core import *
from engine import *
import pygame
from threading import Thread
from templates import *


class Client:

    def __init__(self):
        # Todo realize Game ares
        pygame.init()
        self.current_game_area: GameArea
        self.resolution = (800, 800)
        self.fps = 30
        self.screen = pygame.display.set_mode(self.resolution)

        self.exit = False

        self.settings = Settings(self)
        self.main_menu = MainMenu(self)

        self.switch_game_area(self.main_menu)

        self.run()

    def switch_game_area(self, game_area):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, *self.resolution))
        self.current_game_area = game_area
        self.current_game_area.load()

    def quit(self, e):
        self.exit = True

    def run(self):
        clock = pygame.time.Clock()
        while 1:
            if self.exit:
                break
            for e in pygame.event.get():
                if e.type == pygame.MOUSEMOTION:
                    self.current_game_area.on_mouse_motion(*e.dict['pos'])
                elif e.type == pygame.MOUSEBUTTONUP:
                    self.current_game_area.on_mouse_up(*e.dict['pos'])
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.current_game_area.on_mouse_down(*e.dict['pos'])
                elif e.type == pygame.QUIT:
                    self.exit = True
                elif e.type == pygame.KEYDOWN:
                    self.current_game_area.on_key_down(pygame.key.name(e.key))
            self.current_game_area.render(self.screen)
            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()

Client()