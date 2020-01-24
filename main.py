from core import *
from engine import *
import pygame
from threading import Thread


class Client:

    def __init__(self):
        # Todo realize Game ares
        pygame.init()
        self.resolution = (800, 800)
        self.fps = 30
        self.screen = pygame.display.set_mode(self.resolution)

        main_menu = GameArea()
        bt_new_game = Button(self.resolution, 20, 20, 60, 10, border_color=(255, 255,255), border=2)
        bt_new_game.set_color((255, 0, 0))
        bt_new_game.action_on_mouse_down = nothing
        bt_new_game.action_on_mouse_up = nothing
        bt_new_game.on_hover = lambda self: self.set_color((0, 255, 0))
        bt_new_game.not_hover = lambda self: self.set_color((255, 0, 0))
        bt_new_game.color_on_mouse_down = pygame.Color('blue')
        main_menu.add_objects(bt_new_game)
        # bg = Background(self.resolution, "galaxes\\galaxy_1.jpg")
        # bg.image_mode = '%obj'
        # main_menu.background = bg

        self.current_game_area = main_menu
        self.current_game_area.load()

        self.run()

    def run(self):
        clock = pygame.time.Clock()
        while 1:
            for e in pygame.event.get():
                if e.type == pygame.MOUSEMOTION:
                    self.current_game_area.on_mouse_motion(*e.dict['pos'])
                elif e.type == pygame.MOUSEBUTTONUP:
                    self.current_game_area.on_mouse_up(*e.dict['pos'])
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.current_game_area.on_mouse_down(*e.dict['pos'])

            self.current_game_area.render(self.screen)
            pygame.display.flip()
            clock.tick(self.fps)

Client()