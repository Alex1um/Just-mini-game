from core import *
from engine import *
import pygame
from threading import Thread
from templates import *
from pygame.locals import *


class Client:

    def __init__(self):
        # Todo realize Game ares
        pygame.init()
        pygame.mixer_music.set_volume(0.1)
        self.current_game_area: GameArea
        self.resolution = (800, 800)
        self.fps = 30
        self.screen = pygame.display.set_mode(self.resolution)
        self.full_screen = False

        self.exit = False

        self.pressed_keys = {'left shift': False,
                             'left ctrl': False,
                             'left alt': False}
        self.pressed_keys_set = {'left shift', 'left ctrl', 'left alt'}

        self.settings = Settings(self)
        self.main_menu = MainMenu(self)
        self.space_map_area = SpaceMapScreen(self)
        self.battle_screen = BattleScreen(self)

        self.switch_game_area(self.main_menu)

        self.run()

    def switch_game_area(self, game_area, *args, **kwargs):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, *self.resolution))
        self.current_game_area = game_area
        self.current_game_area.load(self.resolution, *args, **kwargs)

    def switch_resolution(self, width=None, height=None, fullscreen=False):
        w, h = self.resolution
        if width:
            w = width
        if height:
            h = height
        self.resolution = (w, h)
        caption = pygame.display.get_caption()
        cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007
        flags = self.screen.get_flags()
        if fullscreen and not self.full_screen or not fullscreen and self.full_screen:
            flags ^= FULLSCREEN
            self.full_screen = not self.full_screen
        bits = self.screen.get_bitsize()
        # pygame.display.quit()
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.resolution, flags, bits)
        # screen.blit(tmp, (0, 0))
        self.current_game_area.change_resolution(self.resolution)
        pygame.display.set_caption(*caption)
        pygame.key.set_mods(0)  # HACK: work-a-round for a SDL bug??
        pygame.mouse.set_cursor(*cursor)  # Duoas 16-04-2007

    def quit(self, e):
        self.exit = True

    def new_game(self):
        self.game = Game.generate(5, 19)
        self.fraction = random.choice(self.game.fractions)
        self.fraction = self.game.fractions[1]
        self.switch_game_area(self.space_map_area, self.game.space_map)

    def run(self):
        clock = pygame.time.Clock()
        while 1:
            if self.exit:
                break
            for e in pygame.event.get():
                if e.type == pygame.MOUSEMOTION:
                    self.current_game_area.on_mouse_motion(*e.dict['pos'])
                elif e.type == pygame.MOUSEBUTTONUP:
                    self.current_game_area.on_mouse_up(*e.dict['pos'], e.dict['button'])
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.current_game_area.on_mouse_down(*e.dict['pos'], e.dict['button'])
                elif e.type == pygame.QUIT:
                    self.exit = True
                elif e.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(e.key)
                    if key_name in self.pressed_keys_set:
                        self.pressed_keys[key_name] = True
                    self.current_game_area.on_key_down(key_name)
                elif e.type == pygame.KEYUP:
                    key_name = pygame.key.name(e.key)
                    if key_name in self.pressed_keys_set:
                        self.pressed_keys[key_name] = False
            self.current_game_area.update(self)
            self.current_game_area.render(self.screen)
            pygame.display.flip()
            clock.tick(self.fps)
        pygame.quit()


Client()