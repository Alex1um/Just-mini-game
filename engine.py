import time
from typing import *
import pygame
from threading import Thread


DefaultFont = pygame.font.SysFont('Arial', 5)


def nothing(*args, **kwargs):
    pass


class Interface:

    def __init__(self, click: callable, screen):
        self.click_foo = click
        self.screen = screen
        self.buttons = []
        self.sprites = pygame.sprite.Group()


class Object(pygame.sprite.Sprite):

    def __init__(self,
                 resolution,
                 x_rel=0,
                 y_rel=0,
                 w_rel=0,
                 h_rel=0,
                 adopt_size=True,
                 adopt_cords=True):
        super().__init__()
        '''

        :param resolution:
        :param x_rel:
        :param y_rel:
        :param w_rel:
        :param h_rel:
        :param adopt_size: adaptation object size(%) for resolution
        :param adopt_cords: adaptation object cords(%) for resolution
        '''
        self.x_rel, self.y_rel, self.w_rel, self.h_rel = x_rel, y_rel, w_rel, h_rel  # relative
        self.x, self.y = self.x_rel * resolution[0] // 100, self.y_rel * resolution[1] // 100
        self.w, self.h = self.w_rel * resolution[0] // 100, self.h_rel * resolution[1] // 100
        self.adopt_size = adopt_size
        self.adopt_cords = adopt_cords
        self._image = None
        self.image = None
        self.image_mode = '%obj'
        self.image_width = 100
        self.image_height = 100
        # self.color = pygame.color.Color('black')
        self.color = None
        self.text = None
        self.text_shift_x = 0
        self.text_shift_y = 0
        self.font = DefaultFont
        self.rect = self.get_rect()

    def adopt(self, resolution):
        if self.adopt_size:
            self.w, self.h = self.w_rel * resolution[0] // 100, self.h_rel * \
                             resolution[1] // 100
        if self.adopt_cords:
            self.x, self.y = self.x_rel * resolution[0] // 100, self.y_rel * \
                             resolution[1] // 100
        if self.image and self.image_size_mode == '%obj':
            self.image = pygame.transform.scale(self._image, (self.w * self.image_width // 100, self.image_height * self.h // 100))
        self.rect = self.get_rect()

    def get_rect_from_image(self):
        if self.image is not None:
            return self.image.get_rect()
        else:
            raise AttributeError('No image')

    def get_rect(self):
        return pygame.rect.Rect(self.x, self.y, self.w, self.h)

    def image_set(self, image: str, width=100, height=100, size_mode='%img'):
        self._image = pygame.image.load(image)
        self.image_size_mode = size_mode
        self.image_width = width
        self.image_height = height
        if size_mode == 'px':
            self.image = pygame.transform.scale(self._image, (width, height))
        elif size_mode == '%img':
            w, h = self._image.get_width(), self._image.get_height()
            self.image = pygame.transform.scale(self._image,
                                                (w * width // 100,
                                                 h * height // 100))
        elif size_mode == '%obj':
            self.image = pygame.transform.scale(self._image,
                                                (self.w * width // 100,
                                                 self.h * height // 100))

    def color_set(self, color, fmt: str):
        if fmt == 'hsv':
            self.color.hsva = color
        elif fmt == 'rgb':
            self.color.r, self.color.g, self.color.b = color[:3]
            if len(color) > 3:
                self.color.a = color[3]

    def check(self, x, y):
        return self.x <= x <= self.x + self.w and \
            self.y <= y <= self.h + self.y

    def do_action(self, condition: Union[callable, bool], action, timer, *args, **kwargs):
        boolean = True if isinstance(condition, bool) else False
        while 1:
            if boolean and condition:
                action(*args, **kwargs)
            elif condition():
                action(*args, **kwargs)
            time.sleep(timer)

    def connect_hover(self, get_pos: callable, action: callable, delay=0.1):
        Thread(target=self.do_action, args=[lambda: self.check(*get_pos()), action, delay]).start()

    def font_set(self, *args, **kwargs):
        self.font = args[0] if isinstance(args[0], pygame.font.FontType) else \
            pygame.font.SysFont(*args, **kwargs)

    def text_set(self, text, text_color=(0, 0, 0)):
        self.text = self.font.render(text, False, text_color)

    def mouse_down(self, x, y):
        ...

    def mouse_up(self, x, y):
        ...

    def resize(self, w, h):
        self.w, self.h = w, h

    def draw(self, screen):
        if self.text:
            screen.blit(self.text,
                        (self.x + self.text_shift_x,
                         self.y + self.text_shift_y))
        if self.color:
            pygame.draw.rect(screen, self.color, self.get_rect())
        if self.image:
            screen.blit(self.image, self.get_rect())


class Button(Object):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.action_on_mouse_down = nothing
        self.action_on_mouse_up = nothing
        self.color_on_mouse_up = self.color
        self.color_on_mouse_down = pygame.color.Color('Gray')
        self.image_on_mouse_up = None
        self.image_on_mouse_down = None

    def connect_mouse_down(self, action):
        self.action_on_mouse_down = action

    def connect_mouse_up(self, action):
        self.action_on_mouse_up = action

    def mouse_down(self, x, y):
        if self.check(x, y):
            self.action_on_mouse_down()

    def mouse_up(self, x, y):
        if self.check(x, y):
            self.action_on_mouse_up()


class Window(Object):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
