from core import *
from engine import *
import pygame
from threading import Thread


class Client:

    def __init__(self):
        # Todo realize Game ares
        pygame.init()
        self.resolution = (1200, 800)
        self.fps = 30
        self.screen = pygame.display.set_mode(self.resolution)

        self.exit = False

        main_menu = GameArea()
        bt_new_game = Button(self.resolution, 20, 20, 60, 10, border_color=(255, 255, 255), border=2)
        bt_new_game.set_color((150, 150, 150))
        bt_new_game.color_on_mouse_down = pygame.Color('gray')
        bt_new_game.set_text('Начать игру', (0, 255, 0), 43, 50)

        bt_settings = Button(self.resolution, 20, 40, 60, 10, border_color=(255, 255, 255), border=2)
        bt_settings.set_color((150, 150, 150))
        bt_settings.set_text('Настройки', (0, 255, 0), 43, 50)
        bt_settings.color_on_mouse_down = pygame.Color('gray')

        bt_exit = Button(self.resolution, 20, 60, 60, 10, border_color=(255, 255, 255), border=2)
        bt_exit.set_color((150, 150, 150))
        bt_exit.set_text('Выход', (0, 255, 0), 43, 50)
        bt_exit.connect_mouse_down(lambda x: self.quit)
        bt_exit.color_on_mouse_down = pygame.Color('gray')

        main_menu.add_objects(bt_new_game, bt_settings, bt_exit)
        # bg = Background(self.resolution, "galaxes\\galaxy_1.jpg")
        # bg.image_mode = '%obj'
        # main_menu.background = bg

        self.current_game_area = main_menu
        self.current_game_area.load()

        self.run()

    def quit(self):
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
            self.current_game_area.render(self.screen)
            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()

Client()