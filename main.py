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

        main_menu = GameArea()
        settings = GameArea()

        bt_new_game = Button(self.resolution, 20, 20, 60, 10,
                             border_color=(255, 255, 255), border=2)
        bt_new_game.set_color((150, 150, 150))
        bt_new_game.color_on_mouse_down = pygame.Color('gray')
        bt_new_game.set_text('Начать игру', (0, 0, 0))

        bt_settings = Button(self.resolution, 20, 40, 60, 10,
                             border_color=(255, 255, 255), border=2)
        bt_settings.set_color((150, 150, 150))
        bt_settings.set_text('Настройки', (0, 0, 0))
        bt_settings.color_on_mouse_down = pygame.Color('gray')
        bt_settings.connect_mouse_up(lambda x: self.switch_game_area(settings))

        bt_exit = Button(self.resolution, 20, 60, 60, 10,
                         border_color=(255, 255, 255), border=2)
        bt_exit.set_color((150, 150, 150))
        bt_exit.set_text('Выход', (0, 0, 0))
        bt_exit.color_on_mouse_down = pygame.Color('gray')
        bt_exit.connect_mouse_up(self.quit)

        main_menu.add_objects(bt_new_game, bt_settings, bt_exit)

        res_condition = lambda obj, key: key.isdigit() and (key != '0' if len(obj.text) == 0 else len(obj.text) < 4)

        te_res_x = TextEdit(self.resolution, 20, 20, 25, 5, border=2)
        te_res_x.color_default = (200, 200, 200)
        te_res_x.set_color((200, 200, 200))
        te_res_x.color_filling = (160, 160, 160)
        te_res_x.text_condition = res_condition

        te_res_y = TextEdit(self.resolution, 55, 20, 25, 5, border=2)
        te_res_y.color_default = (200, 200, 200)
        te_res_y.set_color((200, 200, 200))
        te_res_y.color_filling = (160, 160, 160)
        te_res_y.text_condition = res_condition
        settings.add_objects(te_res_x, te_res_y)
        # bg = Background(self.resolution, "galaxes\\galaxy_1.jpg")
        # bg.image_mode = '%obj'
        # main_menu.background = bg

        self.switch_game_area(main_menu)

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